# record_verifier - CI-equivalent runner for embedded record verifiers

Production item 2 (owner-approved 2026-10-19, approved after item 4 merged as
PR #870): the readability records embed small fail-safe verifiers, but running
them was manual and inconsistent. This package extracts the verifier from a
record and runs it the way CI would: a scrubbed environment, isolated Python in
a fresh temporary directory, a repo-root cwd, a timeout, and a Python-level
network guard. It is read-only - the repository and records are never modified.

## Exact-line contract

Five records (batch-23, batch-24, batch-25, batch-26 and the paired pilot) use
the exact-line format this tool executes. Inside the record:

~~~text
<!-- verifier:start -->
~~~python
...verbatim verifier source...
~~~
<!-- verifier:end -->

**Expected output line:** VERIFIER OK ...
~~~

The locator is fail-closed: exactly one stripped start marker, exactly one
stripped end marker after it, exactly one stripped ~~~python fence between them,
verbatim code, and one stripped closing ~~~ fence. Any other shape is UNRUN
with the stable diagnostic "no exact-line verifier block found".

Legacy records batch-21/batch-22 carry an embedded-verifier section heading plus
a 3- or 4-tilde python fence but no exact-line markers. They are deliberately
out of scope and fail closed UNRUN with "legacy verifier format (out of scope);
no exact-line verifier markers", never a best-effort extraction.

The expected line is the first line after the block that starts with
**Expected output line:**; the actual value is the last non-empty stdout line
with surrounding backtick quoting stripped. When no expected line is present, a
PASS requires exit code 0 only.

## Usage

    python tools/record_verifier/run.py --record <path|glob> [--record ...]
        [--repo PATH] [--json] [--timeout SECONDS] [--quiet]

- --record is repeatable; the CLI expands globs itself (Windows shells do not).
- Records are de-duplicated in first-seen input order and reported in that order.
- --repo defaults to the git top level containing the first record (fallback:
  that record's directory) and becomes the verifier cwd.
- --timeout defaults to 120 seconds.
- --json prints one deterministic object (screen-reader friendly source only:
  no timestamps, keys sorted); --quiet keeps only the summary line.

## CI-equivalence contract and limits

- Environment allowlist: PATH, SYSTEMROOT/SystemRoot, WINDIR, TEMP, TMP, HOME,
  USERPROFILE, LANG, LC_ALL, PYTHONIOENCODING, PYTHONDONTWRITEBYTECODE, CI.
  Everything else is dropped, so tokens, secrets and proxy variables do not
  reach the verifier; CI=true and PYTHONDONTWRITEBYTECODE=1 are set.
- Isolated Python: sys.executable with -I -B (isolated mode, no bytecode).
- Fresh tempfile.mkdtemp() per record; removed in a finally block.
- Network: a bootstrap installs sys.addaudithook and raises on socket/urllib/
  http audit events; a detected attempt is FAIL with network_blocked=true.
  Honest limit: this is a Python-level guard, not an OS kernel sandbox. Child
  processes inherit the scrubbed environment and no proxy, but are not
  kernel-blocked; records are trusted repository content.
- Timeout expiry is UNRUN (fail-closed), never a PASS.

## Exit codes

    0  every record PASSed
    1  at least one FAIL and no UNRUN
    2  usage error, legacy/malformed record or timeout (UNRUN)

## JSON schema

    {"schema_version": 1,
     "records": [{"record", "status", "exit_code", "expected_line",
                  "expected_match", "network_blocked",
                  "verifier": {"start_line", "end_line", "lines", "lf",
                               "sha256"},
                  "stdout_tail", "stderr_tail", "error"}],
     "summary": {"total", "pass", "fail", "unrun", "exit_code"}}

The aggregate exit code is 2 if any UNRUN/usage, else 1 if any FAIL, else 0
(precedence UNRUN > FAIL > PASS). Contract tests live in
tools/readability_acceptance/tests/test_record_verifier_cli.py, which the
existing CI readability suite already runs - no .github change is needed.
