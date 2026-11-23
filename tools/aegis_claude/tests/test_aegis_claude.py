"""Tests for the Aegis Claude adapter v1 (standard-library unittest)."""

from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.aegis_claude import HOOK_MODULE, POLICY_SCHEMA, __version__
from tools.aegis_claude import cli

BACKUP_GLOB = "claude-settings.json.*"


def run_cli(*argv: str) -> tuple[int, str, str]:
    stdout, stderr = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        try:
            code = cli.main(list(argv))
        except SystemExit as exc:
            code = int(exc.code or 0)
    return code, stdout.getvalue(), stderr.getvalue()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def remove_pycache() -> None:
    for root in (
        REPO_ROOT / "tools" / "aegis_claude",
        REPO_ROOT / "tools" / "aegis_guard",
    ):
        if not root.is_dir():
            continue
        for cache in root.rglob("__pycache__"):
            shutil.rmtree(cache, ignore_errors=True)


def setUpModule() -> None:
    remove_pycache()


def tearDownModule() -> None:
    remove_pycache()


class AdapterTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.settings = self.repo / ".claude" / "settings.json"
        self.policy = self.repo / ".aegis" / "policy.json"
        self.marker = self.repo / ".aegis" / "project.json"
        self.aegis = REPO_ROOT

    def install(self, *extra: str) -> tuple[int, str, str]:
        return run_cli(
            "install",
            "--repo",
            str(self.repo),
            "--aegis-path",
            str(self.aegis),
            "--policy",
            str(self.policy),
            *extra,
        )

    def uninstall(self) -> tuple[int, str, str]:
        return run_cli("uninstall", "--repo", str(self.repo))

    def doctor(self) -> tuple[int, str, str]:
        return run_cli("doctor", "--repo", str(self.repo))

    def adopt(self) -> None:
        write_json(self.marker, {"schema": "aegis.adopt/1"})

    def write_default_policy(self) -> None:
        write_json(self.policy, cli.default_policy())

    def loaded_settings(self) -> dict:
        return read_json(self.settings)

    def all_commands(self, event: str) -> list[str]:
        hooks = self.loaded_settings().get("hooks", {})
        commands: list[str] = []
        for group in hooks.get(event, []):
            if not isinstance(group, dict):
                continue
            for entry in group.get("hooks", []):
                if isinstance(entry, dict) and isinstance(entry.get("command"), str):
                    commands.append(entry["command"])
        return commands

    def our_commands(self, event: str) -> list[str]:
        return [command for command in self.all_commands(event) if HOOK_MODULE in command]

    def backups(self) -> list[Path]:
        directory = self.repo / ".aegis" / "backup"
        if not directory.is_dir():
            return []
        return sorted(directory.glob(BACKUP_GLOB))

    def snapshot_repo(self) -> dict[str, bytes]:
        return {
            str(path.relative_to(self.repo)): path.read_bytes()
            for path in self.repo.rglob("*")
            if path.is_file()
        }


class InstallTests(AdapterTestCase):
    def test_install_creates_default_policy(self) -> None:
        code, _out, err = self.install()
        self.assertEqual(code, 0, err)
        self.assertEqual(read_json(self.policy), cli.default_policy())

    def test_default_policy_allows_only_file_tools(self) -> None:
        self.assertEqual(
            cli.default_policy()["allowed_tools"], ["Read", "Write", "Edit"]
        )

    def test_default_policy_denies_immutable_control_paths(self) -> None:
        protected = (
            "**/.aegis/**",
            "**/.claude/settings.json",
            "**/.claude/settings.local.json",
            "**/.git/**",
        )
        for pattern in protected:
            self.assertIn(pattern, cli.default_policy()["denied_paths"])

    def test_install_creates_one_hook_per_event(self) -> None:
        code, _out, err = self.install()
        self.assertEqual(code, 0, err)
        data = self.loaded_settings()
        session = data["hooks"]["SessionStart"]
        pre = data["hooks"]["PreToolUse"]
        self.assertEqual(len(session), 1)
        self.assertEqual(len(pre), 1)
        self.assertNotIn("matcher", session[0])
        self.assertEqual(pre[0]["matcher"], ".*")
        self.assertEqual(len(self.our_commands("SessionStart")), 1)
        self.assertEqual(len(self.our_commands("PreToolUse")), 1)

    def test_hook_command_has_documented_shape(self) -> None:
        code, _out, err = self.install()
        self.assertEqual(code, 0, err)
        expected = cli.build_hook_command(
            self.aegis.resolve(), self.repo.resolve(), self.policy.resolve()
        )
        self.assertEqual(self.our_commands("SessionStart"), [expected])
        self.assertEqual(self.our_commands("PreToolUse"), [expected])
        self.assertIn("PYTHONPATH=", expected)
        self.assertIn("python -P -m tools.aegis_claude.hook", expected)
        self.assertIn("--repo", expected)
        self.assertIn("--policy", expected)
        # The Aegis checkout path for this repository contains a space, so the
        # generated command must quote it.
        self.assertIn('PYTHONPATH="', expected)

    def test_install_preserves_foreign_hooks_and_keys(self) -> None:
        foreign_session = {
            "hooks": [{"type": "command", "command": "echo foreign-session"}]
        }
        foreign_pre = {
            "matcher": "Write|Edit",
            "hooks": [{"type": "command", "command": "echo foreign-pre"}],
        }
        stop = {"hooks": [{"type": "command", "command": "echo stop"}]}
        original = {
            "permissions": {"allow": ["Read"]},
            "env": {"AEGIS_TEST": "1"},
            "hooks": {
                "SessionStart": [foreign_session],
                "PreToolUse": [foreign_pre],
                "Stop": [stop],
            },
        }
        write_json(self.settings, original)
        code, _out, err = self.install()
        self.assertEqual(code, 0, err)
        data = self.loaded_settings()
        self.assertEqual(data["permissions"], original["permissions"])
        self.assertEqual(data["env"], original["env"])
        self.assertIn(foreign_session, data["hooks"]["SessionStart"])
        self.assertIn(foreign_pre, data["hooks"]["PreToolUse"])
        self.assertEqual(data["hooks"]["Stop"], [stop])
        self.assertEqual(len(self.our_commands("SessionStart")), 1)
        self.assertEqual(len(self.our_commands("PreToolUse")), 1)

    def test_install_is_idempotent(self) -> None:
        self.assertEqual(self.install()[0], 0)
        first = self.settings.read_bytes()
        first_backups = len(self.backups())
        code, out, err = self.install()
        self.assertEqual(code, 0, err)
        self.assertIn("already up to date", out)
        self.assertEqual(self.settings.read_bytes(), first)
        self.assertEqual(len(self.backups()), first_backups)
        self.assertEqual(len(self.our_commands("SessionStart")), 1)
        self.assertEqual(len(self.our_commands("PreToolUse")), 1)

    def test_install_backs_up_preexisting_settings(self) -> None:
        write_json(self.settings, {"permissions": {"allow": []}})
        original = self.settings.read_bytes()
        code, out, err = self.install()
        self.assertEqual(code, 0, err)
        backups = self.backups()
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_bytes(), original)
        self.assertIn("settings backup", out)

    def test_install_does_not_back_up_a_new_settings_file(self) -> None:
        code, _out, err = self.install()
        self.assertEqual(code, 0, err)
        self.assertTrue(self.settings.is_file())
        self.assertEqual(self.backups(), [])

    def test_install_force_replaces_only_our_hook(self) -> None:
        self.assertEqual(self.install()[0], 0)
        data = self.loaded_settings()
        for event in ("SessionStart", "PreToolUse"):
            for group in data["hooks"][event]:
                for entry in group["hooks"]:
                    if HOOK_MODULE in entry["command"]:
                        entry["command"] = (
                            "PYTHONPATH=C:/old python -P -m "
                            "tools.aegis_claude.hook --repo C:/old "
                            "--policy C:/old/policy.json"
                        )
        data["hooks"]["PreToolUse"].append(
            {"hooks": [{"type": "command", "command": "echo keep-me"}]}
        )
        write_json(self.settings, data)
        code, _out, err = self.install("--force")
        self.assertEqual(code, 0, err)
        self.assertEqual(len(self.our_commands("SessionStart")), 1)
        self.assertEqual(len(self.our_commands("PreToolUse")), 1)
        expected = cli.build_hook_command(
            self.aegis.resolve(), self.repo.resolve(), self.policy.resolve()
        )
        self.assertEqual(self.our_commands("SessionStart"), [expected])
        self.assertIn("echo keep-me", self.all_commands("PreToolUse"))
        self.assertNotIn("C:/old", "\n".join(self.our_commands("PreToolUse")))

    def test_install_without_force_keeps_existing_our_command(self) -> None:
        self.assertEqual(self.install()[0], 0)
        data = self.loaded_settings()
        stale = (
            "PYTHONPATH=C:/old python -P -m tools.aegis_claude.hook "
            "--repo C:/old --policy C:/old/policy.json"
        )
        for group in data["hooks"]["SessionStart"]:
            for entry in group["hooks"]:
                entry["command"] = stale
        write_json(self.settings, data)
        original = self.settings.read_bytes()
        code, _out, err = self.install()
        self.assertEqual(code, 0, err)
        self.assertEqual(self.settings.read_bytes(), original)
        self.assertEqual(self.our_commands("SessionStart"), [stale])

    def test_install_requires_guard_main(self) -> None:
        empty_aegis = self.root / "empty-aegis"
        empty_aegis.mkdir()
        code, _out, err = run_cli(
            "install",
            "--repo",
            str(self.repo),
            "--aegis-path",
            str(empty_aegis),
            "--policy",
            str(self.policy),
        )
        self.assertEqual(code, 1)
        self.assertIn("aegis_guard/__main__.py", err)
        self.assertFalse(self.settings.exists())
        self.assertFalse(self.policy.exists())

    def test_install_rejects_vendored_aegis_path(self) -> None:
        vendored = self.repo / "vendor" / "aegis"
        guard_main = vendored / "tools" / "aegis_guard" / "__main__.py"
        guard_main.parent.mkdir(parents=True)
        guard_main.write_text("# guard\n", encoding="utf-8")
        code, _out, err = run_cli(
            "install",
            "--repo",
            str(self.repo),
            "--aegis-path",
            str(vendored),
            "--policy",
            str(self.policy),
        )
        self.assertEqual(code, 1)
        self.assertIn("outside the repository", err)
        self.assertFalse(self.settings.exists())
        self.assertFalse(self.policy.exists())

    @unittest.skipUnless(os.name == "nt", "case-folded vendored check on Windows")
    def test_install_rejects_case_variant_vendored_aegis_path(self) -> None:
        vendored = self.repo / "Vendor" / "Aegis"
        guard_main = vendored / "tools" / "aegis_guard" / "__main__.py"
        guard_main.parent.mkdir(parents=True)
        guard_main.write_text("# guard\n", encoding="utf-8")
        code, _out, err = run_cli(
            "install",
            "--repo",
            str(self.repo),
            "--aegis-path",
            str(vendored).upper(),
            "--policy",
            str(self.policy),
        )
        self.assertEqual(code, 1)
        self.assertIn("outside the repository", err)
        self.assertFalse(self.settings.exists())
        self.assertFalse(self.policy.exists())

    def test_install_rejects_missing_repository(self) -> None:
        code, _out, err = run_cli(
            "install",
            "--repo",
            str(self.root / "missing"),
            "--aegis-path",
            str(self.aegis),
            "--policy",
            str(self.policy),
        )
        self.assertEqual(code, 1)
        self.assertIn("repository", err)

    def test_install_creates_policy_parents(self) -> None:
        self.policy = self.repo / "nested" / "deeper" / "policy.json"
        code, _out, err = self.install()
        self.assertEqual(code, 0, err)
        self.assertTrue(self.policy.is_file())

    def test_install_preserves_existing_policy_bytes(self) -> None:
        self.policy.parent.mkdir(parents=True)
        self.policy.write_bytes(b'{"custom": true}\n')
        original = self.policy.read_bytes()
        code, _out, err = self.install()
        self.assertEqual(code, 0, err)
        self.assertEqual(self.policy.read_bytes(), original)

    def test_install_rejects_invalid_settings_without_overwrite(self) -> None:
        self.settings.parent.mkdir(parents=True)
        self.settings.write_bytes(b"{not json")
        original = self.settings.read_bytes()
        code, _out, err = self.install()
        self.assertEqual(code, 1)
        self.assertIn("not valid JSON", err)
        self.assertEqual(self.settings.read_bytes(), original)
        self.assertEqual(self.backups(), [])

    def test_install_rejects_non_object_hooks(self) -> None:
        write_json(self.settings, {"hooks": []})
        original = self.settings.read_bytes()
        code, _out, err = self.install()
        self.assertEqual(code, 1)
        self.assertIn("hooks", err)
        self.assertEqual(self.settings.read_bytes(), original)

    def test_install_rejects_policy_directory(self) -> None:
        self.policy.mkdir(parents=True)
        code, _out, err = self.install()
        self.assertEqual(code, 1)
        self.assertIn("policy", err)
        self.assertFalse(self.settings.exists())

    def test_install_second_run_adds_a_missing_event_only(self) -> None:
        self.assertEqual(self.install()[0], 0)
        data = self.loaded_settings()
        data["hooks"]["PreToolUse"] = []
        write_json(self.settings, data)
        code, _out, err = self.install()
        self.assertEqual(code, 0, err)
        self.assertEqual(len(self.our_commands("SessionStart")), 1)
        self.assertEqual(len(self.our_commands("PreToolUse")), 1)


class UninstallTests(AdapterTestCase):
    def test_uninstall_removes_only_our_hooks(self) -> None:
        foreign = {"hooks": [{"type": "command", "command": "echo foreign"}]}
        write_json(
            self.settings,
            {"hooks": {"SessionStart": [foreign], "Stop": [foreign]}},
        )
        self.assertEqual(self.install()[0], 0)
        code, _out, err = self.uninstall()
        self.assertEqual(code, 0, err)
        data = self.loaded_settings()
        self.assertEqual(data["hooks"]["SessionStart"], [foreign])
        self.assertEqual(data["hooks"]["Stop"], [foreign])
        self.assertEqual(self.our_commands("SessionStart"), [])
        self.assertEqual(self.our_commands("PreToolUse"), [])

    def test_uninstall_removes_empty_containers(self) -> None:
        self.assertEqual(self.install()[0], 0)
        code, _out, err = self.uninstall()
        self.assertEqual(code, 0, err)
        self.assertEqual(self.loaded_settings(), {})

    def test_uninstall_missing_settings_succeeds(self) -> None:
        code, out, err = self.uninstall()
        self.assertEqual(code, 0, err)
        self.assertIn("no Claude settings", out)
        self.assertFalse(self.settings.exists())

    def test_uninstall_is_idempotent(self) -> None:
        self.assertEqual(self.install()[0], 0)
        self.assertEqual(self.uninstall()[0], 0)
        first = self.settings.read_bytes()
        code, _out, err = self.uninstall()
        self.assertEqual(code, 0, err)
        self.assertEqual(self.settings.read_bytes(), first)

    def test_uninstall_rejects_invalid_settings(self) -> None:
        self.settings.parent.mkdir(parents=True)
        self.settings.write_bytes(b"[]")
        original = self.settings.read_bytes()
        code, _out, err = self.uninstall()
        self.assertEqual(code, 1)
        self.assertIn("JSON object", err)
        self.assertEqual(self.settings.read_bytes(), original)

    def test_uninstall_leaves_unrelated_commands(self) -> None:
        unrelated = {
            "hooks": [
                {"hooks": [{"type": "command", "command": "echo aegis_claude"}]}
            ]
        }
        write_json(self.settings, {"hooks": {"SessionStart": [unrelated]}})
        code, _out, err = self.uninstall()
        self.assertEqual(code, 0, err)
        self.assertEqual(self.loaded_settings()["hooks"]["SessionStart"], [unrelated])

    def test_uninstall_keeps_backups(self) -> None:
        write_json(self.settings, {"permissions": {"allow": []}})
        self.assertEqual(self.install()[0], 0)
        self.assertEqual(len(self.backups()), 1)
        self.assertEqual(self.uninstall()[0], 0)
        self.assertEqual(len(self.backups()), 1)


class DoctorTests(AdapterTestCase):
    def test_doctor_healthy_after_install(self) -> None:
        self.adopt()
        self.assertEqual(self.install()[0], 0)
        code, out, err = self.doctor()
        self.assertEqual(code, 0, err)
        self.assertIn("doctor passed", out)
        self.assertIn("OK   guard:", out)
        self.assertIn("OK   policy:", out)
        self.assertIn("OK   session marker:", out)

    def test_doctor_fails_without_settings(self) -> None:
        code, out, _err = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("settings: missing", out)

    def test_doctor_detects_wrong_policy_schema(self) -> None:
        self.assertEqual(self.install()[0], 0)
        write_json(self.policy, {"schema": "not-aegis"})
        code, out, _err = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("policy schema is not", out)

    def test_doctor_detects_missing_guard(self) -> None:
        fake_aegis = self.root / "fake-aegis"
        (fake_aegis / "tools" / "aegis_claude").mkdir(parents=True)
        (fake_aegis / "tools" / "aegis_claude" / "hook.py").write_text(
            "# hook\n", encoding="utf-8"
        )
        self.write_default_policy()
        command = cli.build_hook_command(fake_aegis, self.repo, self.policy)
        write_json(
            self.settings,
            {
                "hooks": {
                    "SessionStart": [
                        {"hooks": [{"type": "command", "command": command}]}
                    ],
                    "PreToolUse": [
                        {
                            "matcher": ".*",
                            "hooks": [{"type": "command", "command": command}],
                        }
                    ],
                }
            },
        )
        code, out, _err = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("guard: missing", out)

    def test_doctor_detects_missing_hook_module(self) -> None:
        fake_aegis = self.root / "fake-aegis"
        guard_main = fake_aegis / "tools" / "aegis_guard" / "__main__.py"
        guard_main.parent.mkdir(parents=True)
        guard_main.write_text("# guard\n", encoding="utf-8")
        self.write_default_policy()
        command = cli.build_hook_command(fake_aegis, self.repo, self.policy)
        write_json(
            self.settings,
            {
                "hooks": {
                    "SessionStart": [
                        {"hooks": [{"type": "command", "command": command}]}
                    ],
                    "PreToolUse": [
                        {
                            "matcher": ".*",
                            "hooks": [{"type": "command", "command": command}],
                        }
                    ],
                }
            },
        )
        code, out, _err = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("hook: missing", out)

    def test_doctor_is_read_only(self) -> None:
        self.adopt()
        self.assertEqual(self.install()[0], 0)
        before = self.snapshot_repo()
        code, _out, err = self.doctor()
        self.assertEqual(code, 0, err)
        self.assertEqual(self.snapshot_repo(), before)

    def test_doctor_warns_missing_session_marker(self) -> None:
        self.assertEqual(self.install()[0], 0)
        code, out, _err = self.doctor()
        self.assertEqual(code, 0)
        self.assertIn("WARN session marker: missing", out)

    def test_doctor_fails_without_our_hooks(self) -> None:
        foreign = {"hooks": [{"type": "command", "command": "echo foreign"}]}
        write_json(self.settings, {"hooks": {"SessionStart": [foreign]}})
        code, out, _err = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("hook[SessionStart]", out)
        self.assertIn("hook[PreToolUse]", out)


class HookTests(AdapterTestCase):
    def hook(
        self,
        payload: dict | str,
        *,
        policy: Path | None = None,
    ) -> subprocess.CompletedProcess:
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.aegis)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        command = [
            sys.executable,
            "-P",
            "-m",
            "tools.aegis_claude.hook",
            "--repo",
            str(self.repo),
            "--policy",
            str(policy if policy is not None else self.policy),
        ]
        text = payload if isinstance(payload, str) else json.dumps(payload)
        return subprocess.run(
            command,
            cwd=str(self.aegis),
            env=env,
            input=text,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
            check=False,
        )

    def hook_bytes(self, raw: bytes) -> subprocess.CompletedProcess:
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.aegis)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        command = [
            sys.executable,
            "-P",
            "-m",
            "tools.aegis_claude.hook",
            "--repo",
            str(self.repo),
            "--policy",
            str(self.policy),
        ]
        return subprocess.run(
            command,
            cwd=str(self.aegis),
            env=env,
            input=raw,
            capture_output=True,
            timeout=60,
            check=False,
        )

    def prepare(self) -> None:
        self.adopt()
        self.write_default_policy()

    def test_session_start_present(self) -> None:
        self.prepare()
        result = self.hook({"hook_event_name": "SessionStart"})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")

    def test_session_start_camel_case_alias(self) -> None:
        self.prepare()
        result = self.hook({"hook_event_name": "sessionStart"})
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_pretooluse_camel_case_alias(self) -> None:
        self.prepare()
        (self.repo / "src").mkdir()
        (self.repo / "src" / "app.py").write_text("x = 1\n", encoding="utf-8")
        result = self.hook(
            {
                "hook_event_name": "preToolUse",
                "tool_name": "Read",
                "tool_input": {"file_path": "src/app.py"},
                "cwd": str(self.repo),
            }
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_session_start_missing_marker(self) -> None:
        self.write_default_policy()
        result = self.hook({"hook_event_name": "SessionStart"})
        self.assertEqual(result.returncode, 2)
        self.assertIn("session marker", result.stderr)

    def test_session_start_missing_policy(self) -> None:
        self.adopt()
        result = self.hook({"hook_event_name": "SessionStart"})
        self.assertEqual(result.returncode, 2)
        self.assertIn("policy", result.stderr)

    def test_session_start_policy_is_directory(self) -> None:
        self.adopt()
        self.policy.mkdir(parents=True)
        result = self.hook({"hook_event_name": "SessionStart"})
        self.assertEqual(result.returncode, 2)
        self.assertIn("policy", result.stderr)

    def test_session_start_accepts_readable_policy_without_validating_it(self) -> None:
        self.adopt()
        self.policy.parent.mkdir(parents=True, exist_ok=True)
        self.policy.write_text("not json", encoding="utf-8")
        result = self.hook({"hook_event_name": "SessionStart"})
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_malformed_stdin(self) -> None:
        self.prepare()
        result = self.hook("{not json")
        self.assertEqual(result.returncode, 2)
        self.assertIn("not valid JSON", result.stderr)

    def test_empty_stdin(self) -> None:
        self.prepare()
        result = self.hook("")
        self.assertEqual(result.returncode, 2)
        self.assertIn("empty", result.stderr)

    def test_invalid_utf8_stdin(self) -> None:
        self.prepare()
        result = self.hook_bytes(b"\xff\xfe\x00")
        self.assertEqual(result.returncode, 2)
        self.assertIn(b"UTF-8", result.stderr)

    def test_missing_event(self) -> None:
        self.prepare()
        result = self.hook({})
        self.assertEqual(result.returncode, 2)
        self.assertIn("hook_event_name", result.stderr)

    def test_unknown_event(self) -> None:
        self.prepare()
        result = self.hook({"hook_event_name": "Stop"})
        self.assertEqual(result.returncode, 2)
        self.assertIn("unsupported", result.stderr)

    def test_pretooluse_allows_read_inside(self) -> None:
        self.prepare()
        (self.repo / "src").mkdir()
        (self.repo / "src" / "app.py").write_text("x = 1\n", encoding="utf-8")
        result = self.hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Read",
                "tool_input": {"file_path": "src/app.py"},
                "cwd": str(self.repo),
            }
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")

    def test_pretooluse_allows_non_ascii_inside_path(self) -> None:
        self.prepare()
        result = self.hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Read",
                "tool_input": {"file_path": "docs/r\u00e9sum\u00e9.md"},
                "cwd": str(self.repo),
            }
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_pretooluse_allows_write_inside(self) -> None:
        self.prepare()
        result = self.hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Write",
                "tool_input": {"file_path": "notes.txt", "content": "hello"},
                "cwd": str(self.repo),
            }
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_pretooluse_denies_grep_without_path(self) -> None:
        self.prepare()
        result = self.hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Grep",
                "tool_input": {"pattern": "needle"},
                "cwd": str(self.repo),
            },
            policy=self.search_policy(),
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("explicit path", result.stderr)

    def test_pretooluse_denies_glob_without_path(self) -> None:
        self.prepare()
        result = self.hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Glob",
                "tool_input": {"pattern": "**/*.py"},
                "cwd": str(self.repo),
            },
            policy=self.search_policy(),
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("explicit path", result.stderr)

    def test_pretooluse_denies_grep_secrets_path(self) -> None:
        self.prepare()
        (self.repo / "secrets").mkdir()
        result = self.hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Grep",
                "tool_input": {"pattern": "needle", "path": "secrets"},
                "cwd": str(self.repo),
            },
            policy=self.search_policy(),
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("denied by pattern", result.stderr)

    def test_pretooluse_allows_grep_docs_path(self) -> None:
        self.prepare()
        (self.repo / "docs").mkdir()
        result = self.hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Grep",
                "tool_input": {"pattern": "needle", "path": "docs"},
                "cwd": str(self.repo),
            },
            policy=self.search_policy(),
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_pretooluse_allows_glob_docs_path(self) -> None:
        self.prepare()
        (self.repo / "docs").mkdir()
        result = self.hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Glob",
                "tool_input": {"pattern": "**/*.md", "path": "docs"},
                "cwd": str(self.repo),
            },
            policy=self.search_policy(),
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_pretooluse_denies_grep_under_default_policy(self) -> None:
        self.prepare()
        result = self.hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Grep",
                "tool_input": {"pattern": "needle", "path": "docs"},
                "cwd": str(self.repo),
            }
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("not in allowed_tools", result.stderr)

    def test_pretooluse_denies_glob_under_default_policy(self) -> None:
        self.prepare()
        result = self.hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Glob",
                "tool_input": {"pattern": "**/*.md", "path": "docs"},
                "cwd": str(self.repo),
            }
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("not in allowed_tools", result.stderr)

    def test_pretooluse_denies_bash(self) -> None:
        self.prepare()
        result = self.hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Bash",
                "tool_input": {"command": "echo hi"},
                "cwd": str(self.repo),
            }
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("blocked", result.stderr)
        self.assertIn("Bash", result.stderr)

    def test_pretooluse_denies_curl_under_a_bash_allowing_policy(self) -> None:
        self.adopt()
        policy = cli.default_policy()
        policy["allowed_tools"] = ["Read", "Bash"]
        write_json(self.policy, policy)
        result = self.hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Bash",
                "tool_input": {"command": "curl https://example.invalid"},
                "cwd": str(self.repo),
            }
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("network command", result.stderr)

    def test_pretooluse_denies_outside_relative_path(self) -> None:
        self.prepare()
        result = self.hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Read",
                "tool_input": {"file_path": "../outside.txt"},
                "cwd": str(self.repo),
            }
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("traversal", result.stderr)

    def test_pretooluse_denies_absolute_outside_path(self) -> None:
        self.prepare()
        outside = self.root / "outside.txt"
        outside.write_text("secret\n", encoding="utf-8")
        result = self.hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Read",
                "tool_input": {"file_path": str(outside)},
                "cwd": str(self.repo),
            }
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("outside repository", result.stderr)

    def test_pretooluse_denies_dotenv(self) -> None:
        self.prepare()
        (self.repo / ".env").write_text("TOKEN=secret\n", encoding="utf-8")
        result = self.hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Read",
                "tool_input": {"file_path": ".env"},
                "cwd": str(self.repo),
            }
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("denied by pattern", result.stderr)

    def test_pretooluse_denies_write_to_policy(self) -> None:
        self.prepare()
        result = self.hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Write",
                "tool_input": {
                    "file_path": ".aegis/policy.json",
                    "content": "pwned",
                },
                "cwd": str(self.repo),
            }
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("policy file is protected", result.stderr)

    def custom_policy(self) -> Path:
        policy = self.repo / "security" / "policy.json"
        write_json(policy, cli.default_policy())
        return policy

    def search_policy(self) -> Path:
        policy = self.repo / "security" / "search-policy.json"
        data = cli.default_policy()
        data["allowed_tools"] = ["Read", "Write", "Edit", "Grep", "Glob"]
        write_json(policy, data)
        return policy

    def test_pretooluse_denies_write_to_non_default_policy(self) -> None:
        self.adopt()
        policy = self.custom_policy()
        before = policy.read_bytes()
        result = self.hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Write",
                "tool_input": {
                    "file_path": "security/policy.json",
                    "content": "pwned",
                },
                "cwd": str(self.repo),
            },
            policy=policy,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("policy file is protected", result.stderr)
        self.assertEqual(policy.read_bytes(), before)

    def test_pretooluse_denies_edit_to_non_default_policy(self) -> None:
        self.adopt()
        policy = self.custom_policy()
        before = policy.read_bytes()
        result = self.hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Edit",
                "tool_input": {
                    "file_path": "security/policy.json",
                    "old_string": "a",
                    "new_string": "b",
                },
                "cwd": str(self.repo),
            },
            policy=policy,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("policy file is protected", result.stderr)
        self.assertEqual(policy.read_bytes(), before)

    def test_pretooluse_denies_read_of_non_default_policy(self) -> None:
        self.adopt()
        policy = self.custom_policy()
        before = policy.read_bytes()
        result = self.hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Read",
                "tool_input": {"file_path": "security/policy.json"},
                "cwd": str(self.repo),
            },
            policy=policy,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("policy file is protected", result.stderr)
        self.assertEqual(policy.read_bytes(), before)

    def test_pretooluse_denies_hardlink_to_policy(self) -> None:
        self.adopt()
        policy = self.custom_policy()
        link = self.repo / "security" / "policy-link.json"
        try:
            os.link(policy, link)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"hard links unavailable: {exc}")
        before = policy.read_bytes()
        result = self.hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Write",
                "tool_input": {
                    "file_path": "security/policy-link.json",
                    "content": "pwned",
                },
                "cwd": str(self.repo),
            },
            policy=policy,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("policy file is protected", result.stderr)
        self.assertEqual(policy.read_bytes(), before)

    def test_pretooluse_denies_case_variant_policy_path(self) -> None:
        self.adopt()
        policy = self.custom_policy()
        before = policy.read_bytes()
        result = self.hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Write",
                "tool_input": {
                    "file_path": "SECURITY/POLICY.JSON",
                    "content": "pwned",
                },
                "cwd": str(self.repo),
            },
            policy=policy,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("policy file is protected", result.stderr)
        self.assertEqual(policy.read_bytes(), before)

    def test_pretooluse_denies_bash_with_non_default_policy(self) -> None:
        self.adopt()
        policy = self.custom_policy()
        result = self.hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Bash",
                "tool_input": {"command": "echo BASH_RAN"},
                "cwd": str(self.repo),
            },
            policy=policy,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("Bash", result.stderr)

    def test_pretooluse_denies_edit_to_claude_settings(self) -> None:
        self.prepare()
        result = self.hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Edit",
                "tool_input": {
                    "file_path": ".claude/settings.json",
                    "old_string": "a",
                    "new_string": "b",
                },
                "cwd": str(self.repo),
            }
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("denied by pattern", result.stderr)

    def test_pretooluse_denies_write_to_local_settings(self) -> None:
        self.prepare()
        result = self.hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Write",
                "tool_input": {
                    "file_path": ".claude/settings.local.json",
                    "content": "{}",
                },
                "cwd": str(self.repo),
            }
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("denied by pattern", result.stderr)

    def test_pretooluse_denies_write_to_git_metadata(self) -> None:
        self.prepare()
        result = self.hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Write",
                "tool_input": {"file_path": ".git/config", "content": "pwned"},
                "cwd": str(self.repo),
            }
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("denied by pattern", result.stderr)

    def test_pretooluse_denies_read_of_policy(self) -> None:
        self.prepare()
        result = self.hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Read",
                "tool_input": {"file_path": ".aegis/policy.json"},
                "cwd": str(self.repo),
            }
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("policy file is protected", result.stderr)

    def test_pretooluse_denies_webfetch(self) -> None:
        self.prepare()
        result = self.hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "WebFetch",
                "tool_input": {"url": "https://example.invalid"},
                "cwd": str(self.repo),
            }
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("denied by policy", result.stderr)

    def test_pretooluse_missing_tool_name(self) -> None:
        self.prepare()
        result = self.hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_input": {"file_path": "src/app.py"},
            }
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("tool_name", result.stderr)

    def test_pretooluse_missing_tool_input(self) -> None:
        self.prepare()
        result = self.hook(
            {"hook_event_name": "PreToolUse", "tool_name": "Read"}
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("tool_input", result.stderr)

    def test_pretooluse_non_object_tool_input(self) -> None:
        self.prepare()
        result = self.hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Read",
                "tool_input": [],
            }
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("tool_input", result.stderr)

    def test_pretooluse_uses_payload_cwd(self) -> None:
        self.prepare()
        outside = self.root / "outside-dir"
        outside.mkdir()
        (outside / "file.txt").write_text("secret\n", encoding="utf-8")
        result = self.hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Read",
                "tool_input": {"file_path": "file.txt"},
                "cwd": str(outside),
            }
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("outside repository", result.stderr)

    def test_pretooluse_missing_policy(self) -> None:
        self.adopt()
        result = self.hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Read",
                "tool_input": {"file_path": "src/app.py"},
                "cwd": str(self.repo),
            },
            policy=self.repo / "missing-policy.json",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("policy file not found", result.stderr)

    def test_hook_does_not_write_repository(self) -> None:
        self.prepare()
        before = self.snapshot_repo()
        result = self.hook(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Read",
                "tool_input": {"file_path": "src/app.py"},
                "cwd": str(self.repo),
            }
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.snapshot_repo(), before)

    def test_hook_leaves_no_pycache(self) -> None:
        self.prepare()
        result = self.hook({"hook_event_name": "SessionStart"})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(list((self.aegis / "tools" / "aegis_claude").rglob("__pycache__")))
        self.assertFalse(list((self.aegis / "tools" / "aegis_guard").rglob("__pycache__")))


class GuardPathTests(AdapterTestCase):
    def guard(self, tool: str, tool_input: dict, policy: Path | None = None) -> subprocess.CompletedProcess:
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.aegis)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        command = [
            sys.executable,
            "-B",
            "-P",
            "-m",
            "tools.aegis_guard",
            "check",
            "--policy",
            str(policy if policy is not None else self.policy),
            "--repo",
            str(self.repo),
            "--tool",
            tool,
            "--args-json",
            json.dumps(tool_input),
            "--cwd",
            str(self.repo),
        ]
        return subprocess.run(
            command,
            cwd=str(self.aegis),
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
            check=False,
        )

    def prepare(self) -> None:
        self.adopt()
        data = cli.default_policy()
        data["allowed_tools"] = ["Read", "Write", "Edit", "Grep", "Glob"]
        write_json(self.policy, data)

    def test_guard_denies_grep_without_path(self) -> None:
        self.prepare()
        result = self.guard("Grep", {"pattern": "needle"})
        self.assertEqual(result.returncode, 10)
        self.assertIn("explicit path", result.stdout)

    def test_guard_denies_glob_without_path(self) -> None:
        self.prepare()
        result = self.guard("Glob", {"pattern": "**/*.py"})
        self.assertEqual(result.returncode, 10)
        self.assertIn("explicit path", result.stdout)

    def test_guard_denies_grep_secrets_path(self) -> None:
        self.prepare()
        (self.repo / "secrets").mkdir()
        result = self.guard("Grep", {"pattern": "needle", "path": "secrets"})
        self.assertEqual(result.returncode, 10)
        self.assertIn("denied by pattern", result.stdout)

    def test_guard_allows_grep_docs_path(self) -> None:
        self.prepare()
        (self.repo / "docs").mkdir()
        result = self.guard("Grep", {"pattern": "needle", "path": "docs"})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('"allow"', result.stdout)

    def test_guard_allows_glob_docs_path(self) -> None:
        self.prepare()
        (self.repo / "docs").mkdir()
        result = self.guard("Glob", {"pattern": "**/*.md", "path": "docs"})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('"allow"', result.stdout)


class MiscTests(unittest.TestCase):
    def test_version(self) -> None:
        code, out, err = run_cli("--version")
        self.assertEqual(code, 0, err)
        self.assertIn(__version__, out)
        self.assertIn("aegis_claude", out)

    def test_policy_schema_constant(self) -> None:
        self.assertEqual(POLICY_SCHEMA, "aegis.policy/1")


if __name__ == "__main__":
    unittest.main()