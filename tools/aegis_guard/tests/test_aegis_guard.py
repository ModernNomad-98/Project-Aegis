"""Tests for Aegis Guard v1. Standard library only; no network, no shell."""

from __future__ import annotations

import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.aegis_guard import __version__, cli

ARRAY_FIELDS = (
    "allowed_tools",
    "denied_tools",
    "allowed_roots",
    "denied_paths",
    "network_commands",
    "required_session_files",
    "bash_allowlist",
)
REQUIRED_POLICY_FIELDS = {
    "schema",
    "allowed_tools",
    "denied_tools",
    "allowed_roots",
    "denied_paths",
    "deny_outside_repo",
    "network_commands",
    "required_session_files",
}
POLICY_FIELDS = REQUIRED_POLICY_FIELDS | {"bash_allowlist"}
NETWORK_COMMANDS = (
    "curl https://example.com",
    "wget https://example.com",
    "Invoke-WebRequest https://example.com",
    "Invoke-RestMethod https://example.com",
    "ssh host",
    "scp file host:/tmp",
    "sftp host",
    "git push origin main",
    "git fetch origin",
    "git clone https://example.com/repo.git",
    "npm publish",
    "pip install requests",
    "uv pip install requests",
)


class AegisGuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self._temp = tempfile.TemporaryDirectory()
        self.addCleanup(self._temp.cleanup)
        self.base = Path(self._temp.name)
        self.repo = self.base / "repo"
        (self.repo / "docs").mkdir(parents=True)
        (self.repo / "src").mkdir()
        (self.repo / "docs" / "inside.md").write_text("inside\n", encoding="utf-8")
        (self.repo / "src" / "main.py").write_text("print('ok')\n", encoding="utf-8")
        (self.repo / ".env").write_text("SECRET=1\n", encoding="utf-8")
        (self.repo / ".env.local").write_text("LOCAL=1\n", encoding="utf-8")
        (self.repo / ".envrc").write_text("export A=1\n", encoding="utf-8")
        (self.repo / ".envrc.local").write_text("export B=1\n", encoding="utf-8")
        (self.repo / ".ssh").mkdir()
        (self.repo / ".ssh" / "id_test").write_text("key\n", encoding="utf-8")
        (self.repo / ".aws").mkdir()
        (self.repo / ".aws" / "credentials").write_text("aws\n", encoding="utf-8")
        (self.repo / ".gnupg").mkdir()
        (self.repo / ".gnupg" / "secring.gpg").write_text("gpg\n", encoding="utf-8")
        (self.repo / ".git-credentials").write_text("https://token\n", encoding="utf-8")
        (self.repo / "id_rsa").write_text("private\n", encoding="utf-8")
        (self.repo / "cert.pem").write_text("pem\n", encoding="utf-8")
        (self.repo / "server.key").write_text("key\n", encoding="utf-8")
        (self.repo / "secrets").mkdir()
        (self.repo / "secrets" / "token.txt").write_text("token\n", encoding="utf-8")
        (self.repo / "credentials.json").write_text("{}\n", encoding="utf-8")
        (self.repo / ".aegis").mkdir()
        self.write_project()
        (self.repo / ".aegis" / "SESSION.md").write_text("session\n", encoding="utf-8")
        self.outside = self.base / "outside"
        self.outside.mkdir()
        (self.outside / "secret.txt").write_text("outside\n", encoding="utf-8")
        self.policy_path = self.base / "policy.json"
        self.write_policy()

    def policy_data(self) -> dict:
        return {
            "schema": "aegis.policy/1",
            "allowed_tools": ["Read", "Write", "Bash", "NotebookEdit"],
            "denied_tools": ["WebFetch"],
            "allowed_roots": ["."],
            "denied_paths": [],
            "deny_outside_repo": True,
            "network_commands": [],
            "required_session_files": [".aegis/SESSION.md"],
            "bash_allowlist": [
                "echo hello",
                "git status",
                "git --no-pager log",
                "npm test",
                "npm install",
                "pip list",
                "uv pip",
                "python -m unittest",
            ],
        }

    def write_policy(self, remove=(), **overrides) -> None:
        data = self.policy_data()
        data.update(overrides)
        for field in remove:
            data.pop(field, None)
        self.policy_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        self.policy_sha = hashlib.sha256(self.policy_path.read_bytes()).hexdigest()

    def write_project(self, schema: str = "aegis.adopt/1") -> None:
        (self.repo / ".aegis" / "project.json").write_text(
            json.dumps({"schema": schema, "adopted_at": "2026-11-22T00:00:00Z"}),
            encoding="utf-8",
        )

    def invoke(self, *argv: str) -> tuple[int, str, str]:
        out = io.StringIO()
        err = io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(list(argv))
        return code, out.getvalue(), err.getvalue()

    def check(
        self,
        tool: str,
        args: dict | None = None,
        cwd: str | Path | None = None,
        repo: str | Path | None = None,
        args_json: str | None = None,
    ) -> tuple[int, dict | None, str]:
        payload = args_json if args_json is not None else json.dumps(args or {})
        argv = [
            "check",
            "--policy",
            str(self.policy_path),
            "--repo",
            str(repo if repo is not None else self.repo),
            "--tool",
            tool,
            "--args-json",
            payload,
        ]
        if cwd is not None:
            argv += ["--cwd", str(cwd)]
        code, out, err = self.invoke(*argv)
        parsed = json.loads(out) if out.strip() else None
        return code, parsed, err

    def session(self, repo: str | Path | None = None) -> tuple[int, dict | None, str]:
        code, out, err = self.invoke(
            "session",
            "--policy",
            str(self.policy_path),
            "--repo",
            str(repo if repo is not None else self.repo),
        )
        parsed = json.loads(out) if out.strip() else None
        return code, parsed, err

    def assert_allow(self, result: tuple[int, dict | None, str]) -> None:
        code, payload, err = result
        self.assertEqual(code, cli.EXIT_ALLOW, err)
        self.assertIsNotNone(payload)
        self.assertEqual(payload["decision"], "allow")
        self.assertEqual(payload["policy_sha256"], self.policy_sha)
        self.assertRegex(payload["policy_sha256"], r"^[0-9a-f]{64}$")

    def assert_deny(
        self, result: tuple[int, dict | None, str], fragment: str | None = None
    ) -> None:
        code, payload, err = result
        self.assertEqual(code, cli.EXIT_DENY, err)
        self.assertIsNotNone(payload)
        self.assertEqual(payload["decision"], "deny")
        self.assertEqual(payload["policy_sha256"], self.policy_sha)
        self.assertRegex(payload["policy_sha256"], r"^[0-9a-f]{64}$")
        if fragment is not None:
            self.assertIn(fragment, payload["reason"])

    def assert_error(
        self, result: tuple[int, dict | None, str], code: int = cli.EXIT_ERROR
    ) -> None:
        actual, payload, err = result
        self.assertEqual(actual, code, err)
        self.assertIsNone(payload)
        self.assertIn("error", err)

    def test_version(self) -> None:
        code, out, _ = self.invoke("--version")
        self.assertEqual(code, cli.EXIT_ALLOW)
        self.assertIn(__version__, out)

    def test_allow_read_inside(self) -> None:
        self.assert_allow(self.check("Read", {"file_path": "docs/inside.md"}))

    def test_allow_absolute_path_inside(self) -> None:
        self.assert_allow(
            self.check("Read", {"file_path": str(self.repo / "docs" / "inside.md")})
        )

    def test_allow_with_cwd(self) -> None:
        self.assert_allow(
            self.check("Read", {"path": "inside.md"}, cwd=self.repo / "docs")
        )

    def test_allow_notebook_inside(self) -> None:
        (self.repo / "docs" / "note.ipynb").write_text("{}\n", encoding="utf-8")
        self.assert_allow(
            self.check("NotebookEdit", {"notebook_path": "docs/note.ipynb"})
        )

    def test_deny_unlisted_tool_is_fail_closed(self) -> None:
        self.assert_deny(
            self.check("Grep", {"pattern": "x"}), "not in allowed_tools"
        )

    def test_deny_tool_on_denied_list(self) -> None:
        self.assert_deny(self.check("WebFetch", {"url": "https://example.com"}), "denied")

    def test_deny_webfetch_without_url(self) -> None:
        self.assert_deny(self.check("WebFetch", {}))

    def test_deny_read_outside_repository(self) -> None:
        self.assert_deny(
            self.check("Read", {"file_path": str(self.outside / "secret.txt")}),
            "outside repository",
        )

    def test_deny_write_outside_repository(self) -> None:
        self.assert_deny(
            self.check("Write", {"file_path": str(self.outside / "new.txt")}),
            "outside repository",
        )

    def test_deny_traversal(self) -> None:
        for raw in (
            "../outside/secret.txt",
            "docs/../docs/inside.md",
            r"..\outside\secret.txt",
            r"docs\..\docs\inside.md",
        ):
            with self.subTest(raw=raw):
                self.assert_deny(
                    self.check("Read", {"file_path": raw}), "traversal"
                )

    def test_deny_dotenv_paths(self) -> None:
        for raw in (".env", ".env.local", "nested/.env"):
            with self.subTest(raw=raw):
                self.assert_deny(self.check("Read", {"file_path": raw}), "denied by pattern")

    def test_deny_envrc_paths(self) -> None:
        for raw in (".envrc", ".envrc.local", "nested/.envrc"):
            with self.subTest(raw=raw):
                self.assert_deny(
                    self.check("Read", {"path": raw}), "denied by pattern"
                )

    def test_deny_ssh_paths(self) -> None:
        for raw in (".ssh/id_test", ".ssh", ".ssh/config"):
            with self.subTest(raw=raw):
                self.assert_deny(self.check("Read", {"path": raw}), "denied by pattern")

    def test_deny_aws_paths(self) -> None:
        for raw in (".aws/credentials", ".aws"):
            with self.subTest(raw=raw):
                self.assert_deny(self.check("Read", {"path": raw}), "denied by pattern")

    def test_deny_gnupg_paths(self) -> None:
        for raw in (".gnupg/secring.gpg", ".gnupg"):
            with self.subTest(raw=raw):
                self.assert_deny(self.check("Read", {"path": raw}), "denied by pattern")

    def test_deny_git_credentials(self) -> None:
        self.assert_deny(self.check("Read", {"path": ".git-credentials"}), "denied by pattern")

    def test_deny_private_keys(self) -> None:
        for raw in ("id_rsa", "id_rsa.pub", "cert.pem", "server.key"):
            with self.subTest(raw=raw):
                self.assert_deny(self.check("Read", {"path": raw}), "denied by pattern")

    def test_deny_secrets_paths(self) -> None:
        for raw in ("secrets/token.txt", "secrets"):
            with self.subTest(raw=raw):
                self.assert_deny(self.check("Read", {"path": raw}), "denied by pattern")

    def test_deny_credentials_paths(self) -> None:
        for raw in ("credentials.json", "nested/credentials.txt"):
            with self.subTest(raw=raw):
                self.assert_deny(self.check("Read", {"path": raw}), "denied by pattern")

    def test_deny_case_insensitive_secret_path(self) -> None:
        for raw in (".ENV", ".ENVRC", ".ENVRC.LOCAL", ".SSH/ID_TEST", "CERT.PEM"):
            with self.subTest(raw=raw):
                self.assert_deny(self.check("Read", {"path": raw}), "denied by pattern")

    def test_deny_path_outside_allowed_root(self) -> None:
        self.write_policy(allowed_roots=["docs"])
        self.assert_allow(self.check("Read", {"file_path": "docs/inside.md"}))
        self.assert_deny(
            self.check("Read", {"file_path": "src/main.py"}), "allowed roots"
        )

    def test_empty_allowed_roots_denies_paths(self) -> None:
        self.write_policy(allowed_roots=[])
        self.assert_deny(
            self.check("Read", {"file_path": "docs/inside.md"}), "allowed roots"
        )

    def test_repository_containment_is_unconditional(self) -> None:
        outside_root = self.outside
        self.write_policy(allowed_roots=[str(outside_root)])
        self.assert_deny(
            self.check("Read", {"file_path": str(outside_root / "secret.txt")}),
            "outside repository",
        )

    def test_deny_outside_repo_false_does_not_disable_containment(self) -> None:
        self.write_policy(deny_outside_repo=False)
        self.assert_allow(self.check("Read", {"file_path": "docs/inside.md"}))
        self.assert_deny(
            self.check("Read", {"file_path": str(self.outside / "secret.txt")}),
            "outside repository",
        )

    def test_deny_bash_network_commands(self) -> None:
        for command in NETWORK_COMMANDS:
            with self.subTest(command=command):
                self.assert_deny(
                    self.check("Bash", {"command": command}), "network command"
                )

    def test_deny_bash_network_variants(self) -> None:
        for command in (
            "/usr/bin/curl -s https://example.com",
            "GIT   PUSH origin main",
            "python -m pip install requests",
        ):
            with self.subTest(command=command):
                self.assert_deny(
                    self.check("Bash", {"command": command}), "network command"
                )

    def test_deny_git_subcommand_anywhere(self) -> None:
        for command in (
            "git -C . push",
            "git.exe -c x=y push",
            "/usr/bin/git push",
            "git fetch origin",
            "git clone https://example.com/repo.git",
            "git -C . fetch origin",
            "git -C . clone https://example.com/repo.git",
            "git -C . FETCH",
        ):
            with self.subTest(command=command):
                self.assert_deny(
                    self.check("Bash", {"command": command}), "network command"
                )

    def test_deny_npm_subcommand_anywhere(self) -> None:
        for command in (
            "npm --prefix . publish",
            "npm publish redirect",
            "npx publish",
            "npx --yes publish",
            "npm.cmd --workspace app publish",
        ):
            with self.subTest(command=command):
                self.assert_deny(
                    self.check("Bash", {"command": command}), "network command"
                )

    def test_deny_pip_subcommand_anywhere(self) -> None:
        for command in (
            "pip --disable-pip-version-check install x",
            "pip3 install x",
            "pip3 --quiet install x",
            "pip3.12 --quiet install x",
            "python -m pip install x",
        ):
            with self.subTest(command=command):
                self.assert_deny(
                    self.check("Bash", {"command": command}), "network command"
                )

    def test_deny_uv_pip_install_anywhere(self) -> None:
        for command in (
            "uv pip install requests",
            "uv pip --python 3.14 install requests",
            "uv --directory . pip install requests",
            "uv pip3 install requests",
            "uv pip3.12 install requests",
        ):
            with self.subTest(command=command):
                self.assert_deny(
                    self.check("Bash", {"command": command}), "network command"
                )

    def test_deny_network_basename_anywhere(self) -> None:
        for command in (
            "echo curl",
            "printf wget",
            "true ssh",
            "run scp",
            "echo Invoke-RestMethod",
        ):
            with self.subTest(command=command):
                self.assert_deny(
                    self.check("Bash", {"command": command}), "network command"
                )

    def test_deny_nested_bash_c_with_quotes(self) -> None:
        for command in (
            'bash -c "git push"',
            'bash -c "curl x"',
            'powershell -Command "Invoke-WebRequest x"',
            'sh -c "git -C . push"',
        ):
            with self.subTest(command=command):
                self.assert_deny(
                    self.check("Bash", {"command": command}), "escape"
                )

    def test_deny_shell_wrapper_flags(self) -> None:
        for command in (
            "bash -c echo",
            "bash.exe -c echo",
            "sh -c echo",
            "zsh -c echo",
            "cmd /c echo",
            "cmd.exe /C echo",
            "powershell -Command Write-Host",
            "powershell.exe -EncodedCommand Zg==",
            "pwsh -c echo",
        ):
            with self.subTest(command=command):
                self.assert_deny(
                    self.check("Bash", {"command": command}), "shell wrapper"
                )

    def test_deny_shell_wrapper_path(self) -> None:
        for command in (
            "C:/Windows/System32/cmd.exe /c echo",
            "C:/PowerShell/pwsh.exe -Command echo",
            "/bin/bash -c echo",
        ):
            with self.subTest(command=command):
                self.assert_deny(
                    self.check("Bash", {"command": command}), "shell wrapper"
                )

    def test_deny_shell_wrapper_without_network(self) -> None:
        for command in (
            "bash -c echo",
            "cmd /c echo",
            "powershell -Command Write-Host",
        ):
            with self.subTest(command=command):
                self.assert_deny(
                    self.check("Bash", {"command": command}), "shell wrapper"
                )

    def test_deny_shell_metacharacters(self) -> None:
        backtick = chr(96)
        for command in (
            "echo a; echo b",
            "echo a & echo b",
            "echo a | echo b",
            "echo a < in.txt",
            "echo a > out.txt",
            "echo (a)",
            "echo a)",
            "echo hi && git push",
            "echo a || echo b",
            "echo hi\ngit push",
            "echo " + backtick + "curl x" + backtick,
            "echo $(curl x)",
        ):
            with self.subTest(command=command):
                self.assert_deny(
                    self.check("Bash", {"command": command}), "chaining"
                )

    def test_deny_redirects_and_parens(self) -> None:
        for command in (
            "git push>out.log",
            "(git push)",
            "npm publish > out.log",
        ):
            with self.subTest(command=command):
                self.assert_deny(
                    self.check("Bash", {"command": command}), "chaining"
                )

    def test_deny_backslash_paths(self) -> None:
        for command in (
            r"C:\tools\safe.exe --flag",
            r'"C:\Program Files\App\safe.exe" --flag',
            r"C:\repo\docs\file.txt",
            r"echo C:\repo\docs\file.txt",
        ):
            with self.subTest(command=command):
                self.assert_deny(
                    self.check("Bash", {"command": command}), "escape"
                )

    def test_deny_backslash_network_paths(self) -> None:
        for command in (
            r"C:\Windows\System32\curl.exe https://example.com",
            r'"C:\Program Files\Git\bin\git.exe" push',
            r"C:\tools\wget.exe https://example.com",
        ):
            with self.subTest(command=command):
                self.assert_deny(
                    self.check("Bash", {"command": command}), "escape"
                )

    def test_deny_backslash_concatenation(self) -> None:
        for command in (
            r"g\it push",
            r"c\url https://example.com",
            r"gi\t push",
            r"git pu\sh",
        ):
            with self.subTest(command=command):
                self.assert_deny(
                    self.check("Bash", {"command": command}), "escape"
                )

    def test_deny_quote_concatenation(self) -> None:
        for command in (
            "'pu'sh",
            'g"i"t push',
            "'git' push",
            '"git" push',
            "git p'u'sh",
        ):
            with self.subTest(command=command):
                self.assert_deny(
                    self.check("Bash", {"command": command}), "escape"
                )

    def test_deny_dollar_concatenation(self) -> None:
        ifs = "$" + "{IFS}"
        for command in (
            "$'git' push",
            ifs + "curl https://example.com",
            "curl" + ifs,
            "g" + ifs + "it push",
            "$HOME/bin/git push",
        ):
            with self.subTest(command=command):
                self.assert_deny(
                    self.check("Bash", {"command": command}), "escape"
                )

    def test_deny_variable_quote_concatenation(self) -> None:
        ifs = "$" + "{IFS}"
        variable = "$" + "{x}"
        for command in (
            "g'i't push",
            'g"i"t push',
            "g" + ifs + "i" + ifs + "t push",
            "c" + variable + "url",
            r"$'\x67\x69\x74' push",
        ):
            with self.subTest(command=command):
                self.assert_deny(
                    self.check("Bash", {"command": command}), "escape"
                )

    def test_deny_escaped_wrapper_commands(self) -> None:
        for command in (
            'bash -c "echo hi"',
            "cmd /c 'echo hi'",
            r"bash -c g\it push",
            "powershell -EncodedCommand $'...'",
        ):
            with self.subTest(command=command):
                self.assert_deny(
                    self.check("Bash", {"command": command}), "escape"
                )

    def test_deny_shell_chaining(self) -> None:
        for command in (
            "echo hi && git push",
            "echo ok && sftp host",
            "echo a || echo b",
            "echo a | echo b",
            "echo a; echo b",
        ):
            with self.subTest(command=command):
                self.assert_deny(
                    self.check("Bash", {"command": command}), "chaining"
                )

    def test_deny_shell_substitution(self) -> None:
        backtick = chr(96)
        for command in (
            "echo $(curl x)",
            "echo $(git push)",
            "echo " + backtick + "curl x" + backtick,
        ):
            with self.subTest(command=command):
                self.assert_deny(
                    self.check("Bash", {"command": command}), "chaining"
                )

    def test_deny_shell_newline(self) -> None:
        self.assert_deny(
            self.check("Bash", {"command": "echo hi\ngit push"}), "chaining"
        )

    def test_deny_custom_network_command(self) -> None:
        self.write_policy(network_commands=["nc"])
        self.assert_deny(self.check("Bash", {"command": "nc host"}), "network command")
        self.assert_deny(
            self.check("Bash", {"command": "connect nc host"}), "network command"
        )
        self.write_policy(network_commands=["my tool"])
        self.assert_deny(
            self.check("Bash", {"command": "run my tool now"}), "network command"
        )

    def test_deny_malformed_command_quoting(self) -> None:
        self.assert_deny(
            self.check("Bash", {"command": 'echo "unterminated'}), "escape"
        )

    def test_deny_quoted_text(self) -> None:
        for command in (
            'echo "hello world"',
            'echo "git status"',
            "echo 'hello'",
        ):
            with self.subTest(command=command):
                self.assert_deny(
                    self.check("Bash", {"command": command}), "escape"
                )

    def test_allow_bash_safe_commands(self) -> None:
        for command in (
            "echo hello",
            "git status",
            "git --no-pager log",
            "npm test",
            "npm install",
            "pip list",
            "uv pip",
            "python -m unittest",
        ):
            with self.subTest(command=command):
                self.assert_allow(self.check("Bash", {"command": command}))

    def test_bash_default_policy_denies_all_bash(self) -> None:
        self.write_policy(remove=("bash_allowlist",))
        for command in ("echo hello", "git status"):
            with self.subTest(command=command):
                self.assert_deny(
                    self.check("Bash", {"command": command}), "bash_allowlist"
                )
        self.assert_deny(self.check("Bash", {}), "bash_allowlist")

    def test_bash_allowlist_exact_token_match(self) -> None:
        self.write_policy(bash_allowlist=["git status"])
        self.assert_allow(self.check("Bash", {"command": "git status"}))
        self.assert_allow(self.check("Bash", {"command": "git   status"}))
        for command in ("git status --short", "git status extra"):
            with self.subTest(command=command):
                self.assert_deny(
                    self.check("Bash", {"command": command}), "bash_allowlist"
                )

    def test_bash_allowlist_no_prefix_or_glob(self) -> None:
        self.write_policy(bash_allowlist=["git status"])
        for command in ("git statu", "git statu*", "git status*", "git", "g"):
            with self.subTest(command=command):
                self.assert_deny(
                    self.check("Bash", {"command": command}), "bash_allowlist"
                )

    def test_bash_allowlist_blocks_bypass_candidates(self) -> None:
        for command in (
            "git pu*",
            "{git,push}",
            "env bash -c echo",
            "python -c pass",
            "mygit push",
            "git push",
            "curl",
        ):
            with self.subTest(command=command):
                self.assert_deny(self.check("Bash", {"command": command}))

    def test_bash_allowlist_does_not_override_heuristics(self) -> None:
        self.write_policy(bash_allowlist=["git push"])
        self.assert_deny(
            self.check("Bash", {"command": "git push"}), "network command"
        )
        self.write_policy(bash_allowlist=["bash -c echo"])
        self.assert_deny(
            self.check("Bash", {"command": "bash -c echo"}), "shell wrapper"
        )
        self.write_policy(bash_allowlist=["git push>out.log"])
        self.assert_deny(
            self.check("Bash", {"command": "git push>out.log"}), "chaining"
        )

    def test_bash_allowlist_rejects_unlisted_safe_command(self) -> None:
        self.write_policy(bash_allowlist=["echo hello"])
        self.assert_allow(self.check("Bash", {"command": "echo hello"}))
        self.assert_deny(
            self.check("Bash", {"command": "echo hello world"}), "bash_allowlist"
        )

    def test_bash_allowlist_wrong_type(self) -> None:
        self.write_policy(bash_allowlist="git status")
        self.assert_error(self.check("Bash", {"command": "git status"}))

    def test_bash_allowlist_blank_entry(self) -> None:
        self.write_policy(bash_allowlist=["   "])
        self.assert_error(self.check("Bash", {"command": "git status"}))

    def test_bash_allowlist_does_not_affect_other_tools(self) -> None:
        self.write_policy(bash_allowlist=[])
        self.assert_allow(self.check("Read", {"file_path": "docs/inside.md"}))
        self.assert_deny(
            self.check("Bash", {"command": "echo hello"}), "bash_allowlist"
        )

    def test_invalid_denied_glob_is_policy_error(self) -> None:
        self.write_policy(denied_paths=["docs/[z-a]"])
        self.assert_error(self.check("Read", {"file_path": "docs/inside.md"}))

    def test_invalid_denied_glob_blocks_session(self) -> None:
        self.write_policy(denied_paths=["docs/[z-a]"])
        self.assert_error(self.session())

    def test_malformed_policy(self) -> None:
        self.policy_path.write_text("{", encoding="utf-8")
        self.assert_error(self.check("Read", {"file_path": "docs/inside.md"}))

    def test_missing_policy(self) -> None:
        self.policy_path.unlink()
        self.assert_error(self.check("Read", {"file_path": "docs/inside.md"}))

    def test_unknown_policy_field(self) -> None:
        self.write_policy(unknown_field=True)
        self.assert_error(self.check("Read", {"file_path": "docs/inside.md"}))

    def test_missing_policy_field(self) -> None:
        self.write_policy(remove=("denied_paths",))
        self.assert_error(self.check("Read", {"file_path": "docs/inside.md"}))

    def test_wrong_policy_type(self) -> None:
        self.write_policy(allowed_tools="Read")
        self.assert_error(self.check("Read", {"file_path": "docs/inside.md"}))

    def test_wrong_policy_schema(self) -> None:
        self.write_policy(schema="aegis.policy/2")
        self.assert_error(self.check("Read", {"file_path": "docs/inside.md"}))

    def test_malformed_args_json(self) -> None:
        self.assert_error(self.check("Read", args_json="{"), code=cli.EXIT_USAGE)

    def test_args_json_not_object(self) -> None:
        self.assert_error(self.check("Read", args_json="[]"), code=cli.EXIT_USAGE)

    def test_duplicate_args_json_key(self) -> None:
        self.assert_error(
            self.check(
                "Read",
                args_json='{"file_path": "docs/inside.md", "file_path": ".env"}',
            ),
            code=cli.EXIT_USAGE,
        )

    def test_malformed_path_argument(self) -> None:
        self.assert_error(
            self.check("Read", {"file_path": 5}), code=cli.EXIT_USAGE
        )
        self.assert_error(
            self.check("Read", {"file_path": ""}), code=cli.EXIT_USAGE
        )

    def test_malformed_command_argument(self) -> None:
        self.assert_error(
            self.check("Bash", {"command": ["curl"]}), code=cli.EXIT_USAGE
        )

    def test_empty_tool_is_usage_error(self) -> None:
        self.assert_error(self.check("", {}), code=cli.EXIT_USAGE)

    def test_missing_cli_argument(self) -> None:
        code, out, err = self.invoke(
            "check", "--policy", str(self.policy_path), "--repo", str(self.repo)
        )
        self.assertEqual(code, cli.EXIT_USAGE)
        self.assertEqual(out, "")
        self.assertIn("error", err)

    def test_no_subcommand(self) -> None:
        code, out, err = self.invoke()
        self.assertEqual(code, cli.EXIT_USAGE)
        self.assertEqual(out, "")
        self.assertIn("error", err)

    def test_missing_repository(self) -> None:
        self.assert_error(
            self.check("Read", {"file_path": "docs/inside.md"}, repo=self.base / "missing")
        )

    def test_missing_cwd(self) -> None:
        self.assert_error(
            self.check("Read", {"file_path": "docs/inside.md"}, cwd=self.base / "missing")
        )

    def test_policy_sha_printed(self) -> None:
        allow = self.check("Read", {"file_path": "docs/inside.md"})
        deny = self.check("Read", {"file_path": ".env"})
        self.assert_allow(allow)
        self.assert_deny(deny)
        self.assertEqual(allow[1]["policy_sha256"], deny[1]["policy_sha256"])
        self.assertEqual(allow[1]["policy_sha256"], self.policy_sha)

    def test_missing_session_marker(self) -> None:
        (self.repo / ".aegis" / "project.json").unlink()
        self.assert_deny(self.session(), "project.json")

    def test_session_allow(self) -> None:
        self.assert_allow(self.session())

    def test_session_wrong_schema(self) -> None:
        self.write_project("aegis.adopt/2")
        self.assert_deny(self.session(), "aegis.adopt/1")

    def test_session_invalid_json(self) -> None:
        (self.repo / ".aegis" / "project.json").write_text("{", encoding="utf-8")
        self.assert_deny(self.session(), "invalid JSON")

    def test_session_missing_required_file(self) -> None:
        (self.repo / ".aegis" / "SESSION.md").unlink()
        self.assert_deny(self.session(), "SESSION.md")

    def test_session_required_file_traversal(self) -> None:
        self.write_policy(required_session_files=["../outside/secret.txt"])
        self.assert_error(self.session())

    def test_session_required_file_device_path(self) -> None:
        self.write_policy(required_session_files=["docs/CON"])
        self.assert_error(self.session())

    def test_windows_backslash_paths(self) -> None:
        self.assert_allow(self.check("Read", {"file_path": r"docs\inside.md"}))
        self.assert_deny(
            self.check("Read", {"file_path": r".ssh\id_test"}), "denied by pattern"
        )
        self.assert_deny(
            self.check("Read", {"file_path": r"docs\..\docs\inside.md"}),
            "traversal",
        )

    def test_unc_and_device_paths(self) -> None:
        for raw in (
            r"\\server\share\secret.txt",
            r"\\.\C:\Windows\win.ini",
            r"\\?\C:\Windows\win.ini",
            r"C:relative.txt",
            r"docs\CON",
        ):
            with self.subTest(raw=raw):
                self.assert_deny(
                    self.check("Read", {"file_path": raw}), "UNC or device"
                )

    @unittest.skipUnless(os.name == "nt", "Windows case-insensitive containment")
    def test_windows_repository_case_insensitive(self) -> None:
        alt_repo = str(self.repo).upper()
        self.assert_allow(
            self.check(
                "Read",
                {"file_path": str(self.repo / "docs" / "inside.md")},
                repo=alt_repo,
            )
        )

    def test_symlink_or_junction_escape_is_denied(self) -> None:
        file_link = self.repo / "docs" / "escape.md"
        raw = "docs/escape.md"
        try:
            file_link.symlink_to(self.outside / "secret.txt")
        except (OSError, NotImplementedError):
            if os.name != "nt":
                self.skipTest("symlink and junction creation are unavailable")
            directory_link = self.repo / "docs" / "escape_dir"
            created = subprocess.run(
                [
                    "cmd",
                    "/c",
                    "mklink",
                    "/J",
                    str(directory_link),
                    str(self.outside),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            if created.returncode != 0:
                self.skipTest("symlink and junction creation are unavailable")
            raw = "docs/escape_dir/secret.txt"
        self.assert_deny(
            self.check("Read", {"file_path": raw}), "outside repository"
        )

    def test_schema_contract(self) -> None:
        schema = json.loads(
            (REPO_ROOT / "tools" / "aegis_guard" / "policy.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(
            schema["$schema"], "https://json-schema.org/draft/2020-12/schema"
        )
        self.assertEqual(schema["type"], "object")
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(set(schema["required"]), REQUIRED_POLICY_FIELDS)
        self.assertEqual(set(schema["properties"]), POLICY_FIELDS)
        self.assertEqual(schema["properties"]["schema"]["const"], "aegis.policy/1")
        self.assertEqual(
            schema["properties"]["deny_outside_repo"]["type"], "boolean"
        )
        self.assertEqual(schema["properties"]["bash_allowlist"]["default"], [])
        for field in ARRAY_FIELDS:
            with self.subTest(field=field):
                self.assertEqual(schema["properties"][field]["type"], "array")
                self.assertEqual(
                    schema["properties"][field]["items"]["type"], "string"
                )
                self.assertEqual(
                    schema["properties"][field]["items"]["minLength"], 1
                )

    def test_no_shell_or_network_imports(self) -> None:
        source = Path(cli.__file__).read_text(encoding="utf-8")
        for module in ("subprocess", "socket", "urllib", "http", "requests"):
            with self.subTest(module=module):
                self.assertIsNone(
                    re.search(
                        rf"(?m)^\s*(?:import|from)\s+{module}\b", source
                    )
                )
        for marker in (
            "os.system(",
            "os.popen(",
            "shell=True",
            "urlopen(",
            "eval(",
            "exec(",
        ):
            with self.subTest(marker=marker):
                self.assertNotIn(marker, source)


if __name__ == "__main__":
    unittest.main()
