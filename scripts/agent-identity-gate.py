#!/usr/bin/env python3
"""Manual pre-first-commit agent identity gate (DS-R1b).

This is an explicitly manual check, not an installed hook. It reads the
effective Git identity and a supported explicit-source matrix, prints a
deterministic ACCEPT or STOP verdict and exits 0/2. It is best-effort and not
a security boundary: --no-verify, later --author/amend changes and commands
that never run this script are outside its control.

Design requirements: strict raw git var validation; key-exact config reads
with duplicate rejection; same-scope/same-role config pairing; per-field
justification where 'inherited_fallback' is used only when the global value
equals the effective one; command-scope config decoded by Git itself; dedicated
aegis.ownerName/aegis.ownerEmail owner separation, where the owner email is
compared case-insensitively and a name-only match is advisory output.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from collections import namedtuple

REASON_CONFIG_DUPLICATE = "E_CONFIG_DUPLICATE"
REASON_CONFIG_ERROR = "E_CONFIG_ERROR"
REASON_ENV_CONTROL = "E_ENV_CONTROL"
REASON_MALFORMED_IDENT = "E_MALFORMED_IDENT"
REASON_NO_EXPLICIT_SOURCE = "E_NO_EXPLICIT_SOURCE"
REASON_NO_OWNER = "E_OWNER_MISSING"
REASON_OWNER_EFFECTIVE = "E_OWNER_EFFECTIVE"
REASON_UNJUSTIFIED_FIELD = "E_UNJUSTIFIED_FIELD"
REASON_INTERNAL = "E_INTERNAL"

IDENT_RE = re.compile(
    r"^(?P<name>[^<>\n\r]+) <(?P<email>[^<>\n\r]+)> "
    r"(?P<time>[0-9]+) (?P<tz>[+-][0-9]{4})$"
)
CONTROL_RE = re.compile(r"[\x00-\x1f\x7f]")


class GateStop(Exception):
    def __init__(self, reason, detail):
        super().__init__(reason + ": " + detail)
        self.reason = reason
        self.detail = detail


Identity = namedtuple("Identity", "name email")


def _git(args, cwd, env):
    return subprocess.run(
        ["git"] + list(args), cwd=cwd, env=env,
        capture_output=True, text=True, encoding="utf-8",
        errors="strict", check=False,
    )


def validate_ident(raw, role):
    """Strictly parse one raw git var identity line; reject any control/newline."""
    if not isinstance(raw, str) or raw == "":
        raise GateStop(REASON_MALFORMED_IDENT,
                       role + " raw output is empty")
    text = raw
    if text.endswith("\n"):
        text = text[:-1]
        if text.endswith("\r"):
            text = text[:-1]
    if "\n" in text or "\r" in text:
        raise GateStop(REASON_MALFORMED_IDENT,
                       role + " raw output has internal newline")
    if CONTROL_RE.search(text):
        raise GateStop(REASON_MALFORMED_IDENT,
                       role + " raw output has control characters")
    match = IDENT_RE.fullmatch(text)
    if match is None:
        raise GateStop(REASON_MALFORMED_IDENT,
                       role + " raw output is not a strict identity line")
    name = match.group("name")
    email = match.group("email")
    if not name or not email:
        raise GateStop(REASON_MALFORMED_IDENT, role + " name/email is empty")
    if name.strip() != name or not name.strip():
        raise GateStop(REASON_MALFORMED_IDENT,
                       role + " name has leading/trailing/only whitespace")
    if email.strip() != email or not email.strip():
        raise GateStop(REASON_MALFORMED_IDENT,
                       role + " email has leading/trailing/only whitespace")
    if re.search(r"\s", email):
        raise GateStop(REASON_MALFORMED_IDENT, role + " email contains whitespace")
    return Identity(name, email)


def read_identity(cwd, env=None):
    env = dict(os.environ if env is None else env)
    out = {}
    for role, key in (("author", "GIT_AUTHOR_IDENT"),
                      ("committer", "GIT_COMMITTER_IDENT")):
        proc = _git(["var", key], cwd, env)
        if proc.returncode != 0:
            raise GateStop(REASON_MALFORMED_IDENT,
                           role + " identity unavailable from git var")
        out[role] = validate_ident(proc.stdout, role)
    return out


def _read_all_config(cwd, env, scope, key):
    args = ["config"]
    if scope == "local":
        args.append("--local")
    elif scope == "worktree":
        args.append("--worktree")
    elif scope == "global":
        args.append("--global")
    else:
        raise GateStop(REASON_INTERNAL, "unknown config scope")
    proc = _git(args + ["--null", "--get-all", key], cwd, env)
    if proc.returncode == 1:
        return []
    if proc.returncode != 0:
        raise GateStop(REASON_CONFIG_ERROR,
                       scope + " config read failed for " + key)
    chunks = proc.stdout.split("\x00")
    if chunks and chunks[-1] == "":
        chunks = chunks[:-1]
    return chunks


def _config_entries(cwd, env, key):
    """[(scope, value)] for key, exactly as Git itself reports them.

    The command scope is the only scope this gate cannot read with a
    --local/--worktree/--global flag, and Git's internal
    GIT_CONFIG_PARAMETERS format is shell-quoted. Delegating the decode to
    Git's own --show-scope/--null output removes a hand-written parser that was
    narrower than Git: both the 'key=value' and 'key'='value' forms, quoted
    apostrophes, literal backslashes, '=' inside a value and Git's
    case-insensitive key matching behave exactly as Git behaves. A malformed
    value makes Git fail, which STOPs as E_CONFIG_ERROR instead of being
    silently tolerated. Requires Git >= 2.26 for --show-scope; an older Git
    fails closed as E_CONFIG_ERROR.
    """
    proc = _git(["config", "--show-scope", "--null", "--get-all", key],
                cwd, env)
    if proc.returncode == 1:
        return []
    if proc.returncode != 0:
        raise GateStop(REASON_CONFIG_ERROR, "config read failed for " + key)
    chunks = proc.stdout.split("\x00")
    if chunks and chunks[-1] == "":
        chunks = chunks[:-1]
    if len(chunks) % 2:
        raise GateStop(REASON_CONFIG_ERROR,
                       "config scope output is malformed for " + key)
    return list(zip(chunks[0::2], chunks[1::2]))


def _collect_command_config(cwd, env):
    """Command-scope user.name/email values, decoded by Git itself.

    Only the 'command' scope is kept, so explicit local/worktree identity is
    never reclassified as command scope. Duplicate keys in either
    GIT_CONFIG_PARAMETERS or GIT_CONFIG_COUNT form are rejected, including
    case-variant spellings, because Git matches config keys case-insensitively
    and --get-all returns every command-scope value for the key.
    """
    values = {}
    for key in ("user.name", "user.email"):
        values[key] = [value for scope, value in _config_entries(cwd, env, key)
                       if scope == "command"]
    for key, found in values.items():
        if len(found) > 1:
            raise GateStop(REASON_CONFIG_DUPLICATE,
                           "duplicate command config " + key)
    return values


def _check_value_text(value, label):
    if value is None:
        raise GateStop(REASON_CONFIG_ERROR, label + " is missing")
    if not value.strip():
        raise GateStop(REASON_CONFIG_ERROR, label + " is empty/whitespace")
    if "\n" in value or "\r" in value or CONTROL_RE.search(value):
        raise GateStop(REASON_CONFIG_ERROR,
                       label + " contains newline/control characters")


def _check_owner_text(value, label, is_email):
    """Validate the RAW owner value; trimming never precedes validation."""
    if not value.strip():
        raise GateStop(REASON_NO_OWNER, label + " is empty/whitespace")
    _check_value_text(value, label)
    if value != value.strip():
        raise GateStop(REASON_CONFIG_ERROR,
                       label + " has leading/trailing whitespace")
    if is_email and re.search(r"\s", value):
        raise GateStop(REASON_CONFIG_ERROR, label + " contains whitespace")


def _worktree_config_enabled(cwd, env):
    proc = _git(["config", "--bool", "--get",
                 "extensions.worktreeConfig"], cwd, env)
    if proc.returncode == 1:
        return False
    if proc.returncode != 0:
        raise GateStop(REASON_CONFIG_ERROR,
                       "worktree config detection failed")
    value = proc.stdout.strip().lower()
    if value == "true":
        return True
    if value == "false":
        return False
    raise GateStop(REASON_CONFIG_ERROR,
                   "worktree config detection returned a non-boolean value")


def _owner_value(cwd, env, key, label, is_email):
    values = _read_all_config(cwd, env, "local", key)
    if len(values) == 0:
        raise GateStop(REASON_NO_OWNER, label + " is missing")
    if len(values) > 1:
        raise GateStop(REASON_CONFIG_DUPLICATE,
                       label + " has duplicate values")
    raw = values[0]
    _check_owner_text(raw, label, is_email)
    return raw


def _global_identity_fields(cwd, env):
    """Fallback = global config only; local/worktree explicit config excluded.

    Fallback values are validated with the same rule as local config values,
    so the equality test in evaluate() compares like with like.
    """
    fields = {}
    for label, key in (("name", "user.name"), ("email", "user.email")):
        chunks = _read_all_config(cwd, env, "global", key)
        if len(chunks) > 1:
            raise GateStop(REASON_CONFIG_DUPLICATE,
                           "global config duplicate " + key)
        value = chunks[0] if chunks else ""
        if value:
            _check_value_text(value, "global " + label)
        fields[label] = value
    return fields


def config_pairs(cwd, env, effective):
    """Return qualifying same-scope, same-role config pairs."""
    pairs = []
    scopes = []
    scope_names = ["local"]
    if _worktree_config_enabled(cwd, env):
        scope_names.append("worktree")
    for scope in scope_names:
        names = _read_all_config(cwd, env, scope, "user.name")
        emails = _read_all_config(cwd, env, scope, "user.email")
        for label, found in (("name", names), ("email", emails)):
            if len(found) > 1:
                raise GateStop(REASON_CONFIG_DUPLICATE,
                               scope + " " + label + " has duplicate values")
            if found:
                _check_value_text(found[0], scope + " " + label)
        if names and emails:
            scopes.append((scope, names[0], emails[0]))
    commands = _collect_command_config(cwd, env)
    for label, found in (("name", commands["user.name"]),
                         ("email", commands["user.email"])):
        if found:
            _check_value_text(found[0], "command " + label)
    if commands["user.name"] and commands["user.email"]:
        scopes.append(("command", commands["user.name"][0],
                       commands["user.email"][0]))
    author = effective["author"]
    committer = effective["committer"]
    for scope, name, email in scopes:
        if name == author.name and email == author.email:
            pairs.append((scope, "author", name, email))
        elif name == committer.name and email == committer.email:
            pairs.append((scope, "committer", name, email))
    return pairs


def _env_field(env, key, effective_field, fallback_field, role, field):
    raw = env.get(key)
    if raw is None or raw == "":
        return None
    if "\n" in raw or "\r" in raw or CONTROL_RE.search(raw):
        raise GateStop(REASON_ENV_CONTROL,
                       role + " " + field + " env has newline/control")
    if raw != effective_field:
        return None
    if fallback_field and raw == fallback_field:
        return None
    return raw


def evaluate(cwd, env=None):
    env = dict(os.environ if env is None else env)
    owner_name = _owner_value(cwd, env, "aegis.ownerName", "owner name", False)
    owner_email = _owner_value(cwd, env, "aegis.ownerEmail", "owner email", True)
    effective = read_identity(cwd, env)
    pairs = config_pairs(cwd, env, effective)
    global_fields = _global_identity_fields(cwd, env)
    author = effective["author"]
    committer = effective["committer"]
    fields = {
        ("author", "name"): author.name,
        ("author", "email"): author.email,
        ("committer", "name"): committer.name,
        ("committer", "email"): committer.email,
    }
    fallback_fields = {
        ("author", "name"): global_fields["name"],
        ("author", "email"): global_fields["email"],
        ("committer", "name"): global_fields["name"],
        ("committer", "email"): global_fields["email"],
    }
    explicit = {}
    for (role, field), value in fields.items():
        var = ("GIT_AUTHOR_NAME" if (role, field) == ("author", "name")
               else "GIT_AUTHOR_EMAIL" if (role, field) == ("author", "email")
               else "GIT_COMMITTER_NAME" if (role, field) == ("committer", "name")
               else "GIT_COMMITTER_EMAIL")
        fb = fallback_fields.get((role, field), "")
        explicit[(role, field)] = _env_field(env, var, value, fb, role, field)
    explicit_pairs = {}
    same_identity = (author.name == committer.name
                     and author.email == committer.email)
    for scope, role, name, email in pairs:
        roles = ("author", "committer") if same_identity else (role,)
        for justified_role in roles:
            explicit_pairs[(justified_role, "name")] = "config:" + scope
            explicit_pairs[(justified_role, "email")] = "config:" + scope
    reasons = {}
    for (role, field), value in fields.items():
        fb = fallback_fields.get((role, field), "")
        env_val = explicit.get((role, field))
        if (role, field) in explicit_pairs:
            reasons[(role, field)] = explicit_pairs[(role, field)]
        elif env_val is not None:
            reasons[(role, field)] = "env"
        elif fb and fb == value:
            reasons[(role, field)] = "inherited_fallback"
        else:
            raise GateStop(REASON_UNJUSTIFIED_FIELD,
                           role + " " + field + " is not justified by an "
                           "explicit source or an equal global fallback")
    has_source = bool(pairs) or any(value is not None for value in explicit.values())
    if not has_source:
        raise GateStop(REASON_NO_EXPLICIT_SOURCE,
                       "no supported explicit source; inherited-global-only/auto identity is not a pass")
    # Owner decision (2026-10-29): STOP when the effective email equals the
    # recorded owner email case-insensitively, or when name AND email both
    # match. The conjunction is subsumed by the email comparison, so it is
    # implemented once here; a name-only match is advisory output, never STOP.
    owner_email_key = owner_email.casefold()
    owner_name_key = owner_name.casefold()
    advisories = []
    for role, ident in effective.items():
        if ident.email.casefold() == owner_email_key:
            raise GateStop(REASON_OWNER_EFFECTIVE,
                           role + " effective email matches the recorded owner email")
        if ident.name.casefold() == owner_name_key:
            advisories.append(role + "-name-matches-owner")
    provenance = []
    for scope, role, name, email in pairs:
        provenance.append("config:" + scope + ":" + role)
    for (role, field), source in explicit.items():
        if source is not None:
            provenance.append("env:" + role + "-" + field)
    provenance = sorted(set(provenance))
    return {
        "author": author,
        "committer": committer,
        "provenance": provenance,
        "advisories": sorted(set(advisories)),
        "justification": sorted(
            role + "-" + field + ":" + reasons[(role, field)]
            for role, field in reasons),
    }


def format_accept(result):
    author = result["author"]
    committer = result["committer"]
    advisories = ",".join(result["advisories"]) or "none"
    return ("ACCEPT effective_author="
            + repr(author.name + " <" + author.email + ">")
            + " effective_committer="
            + repr(committer.name + " <" + committer.email + ">")
            + " provenance=" + ",".join(result["provenance"])
            + " justification=" + ",".join(result["justification"])
            + " advisories=" + advisories)


def format_stop(reason, detail):
    return "STOP reason=" + reason + " detail=" + detail.replace("\n", " ").replace("\r", " ")


def main():
    try:
        cwd = os.getcwd()
        result = evaluate(cwd)
    except GateStop as error:
        print(format_stop(error.reason, error.detail))
        return 2
    except Exception as error:  # fail closed, deterministic, no traceback
        print(format_stop(REASON_INTERNAL, type(error).__name__))
        return 2
    print(format_accept(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
