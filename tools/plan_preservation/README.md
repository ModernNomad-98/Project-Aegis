# Plan-preservation linter

A deterministic, offline checker that flags two failure classes in plan bodies:
**dropped requirement sentences** between revisions, and **stale abbreviated
basis references** (short commit hashes that no longer match the declared
basis), plus a UTF-8 size-cap check. It reports findings only: it never edits
a plan and never calls the network.

Design of record: the accepted plan revision 4 for owner-approved production
item 1 (2026-10-19). Standard library only; no third-party dependency.

## Usage

    python tools/plan_preservation/lint.py --previous PREV [--previous PREV ...] \
        --new NEW [--declared-basis HEX] [--live-main HEX] [--allow-sha HEX ...] \
        [--size-cap BYTES] [--json] [--quiet]

- `--previous PREV` - previous plan body; repeatable and required (one or more).
- `--new NEW` - new plan body; `-` reads standard input. Only `--new` may read
  standard input.
- `--declared-basis HEX` - the commit the plan declares as its basis
  (7-64 lowercase hex characters). Required for the stale-basis check: without
  it that check is skipped and a warning is printed.
- `--live-main HEX` - the current live main commit (7-64 lowercase hex),
  accepted like the declared basis.
- `--allow-sha HEX` - an additional accepted hash value (repeatable; 7-64
  lowercase hex). Use it for pinned hashes and other legitimate references the
  qualifier list does not recognise.
- `--size-cap BYTES` - UTF-8 byte cap for the new body; default **15,360**.
- `--json` - emit a deterministic JSON record with sort_keys and no timestamps.
- `--quiet` - print only the `RESULT:` line in human output.

## Exit codes

- **0** - clean: no findings.
- **1** - findings: dropped requirements, stale basis references, or size over cap.
- **2** - usage or input error: missing file, malformed hex value, previous
  input on standard input, invalid `--size-cap`.
- **3** - internal error (reported on standard error).

## Requirement extraction

Requirement-bearing lines are numbered AC rows (lines matching
`N. **AC<n>`) and lines carrying an obligation keyword (must, never, exactly,
zero, at most, non-zero, required, immutable, superseded, shall). Units are
semicolon-separated clauses of at least 8 characters; an AC row also counts as
a whole line. Each unit is normalised (NFKC, straight quotes, emphasis and
backticks stripped, whitespace collapsed, lowercased, terminal punctuation
stripped) and checked as a substring of the normalised new body, so pure
reformatting is tolerated while a dropped sentence is flagged.

**Limitation:** keyword-free requirement text is not extracted. This is a
heuristic, not a completeness proof; synonym rewording evades the matcher.

## Stale basis references

Candidates are 7-40 character lowercase hex tokens delimited from longer hex
runs, and only tokens containing at least one a-f letter are considered
(pure-decimal identifiers are rejected). A token is accepted only when one of
these holds:

1. It equals or is a prefix of `--declared-basis`, `--live-main`, or an
   `--allow-sha` value.
2. **Cell-level content-hash exemption:** the token's pipe-delimited table cell,
   trimmed and backtick-stripped, is exactly the token (for example a Blob
   column cell holding one 40-hex hash). A cell such as `Blob at 5a1d8c07` is
   evidence prose, not an exact-token cell, and is *not* exempt.
3. **Same-line qualifier, case-insensitive:** superseded, equality verified,
   equal at, or not a record merge. Any qualifier on the line suppresses every
   token on that line (documented coarseness; token-scoped qualifiers are a
   non-goal).
4. **Recorded-hash marker:** `sha256=`, `sha256:`, `sha256` followed by a
   space, `binding=sha256` followed by a space, or a skill reference written as
   a name, a space, an at sign and a space. Those are evidence hashes, not
   basis references.

Everything else is reported as a stale-basis finding with token, line and
reason.

## Size cap

The new body is measured in UTF-8 bytes (multibyte characters count by their
encoded bytes) against `--size-cap` (default 15,360). Over-cap is a finding.

## Output

Human output reports size, dropped requirements, stale basis references,
warnings, and a final `RESULT:` line. `--json` emits a deterministic record
with the keys: tool, version, model, inputs, size, dropped_requirements,
stale_basis, warnings, summary, exit_code. Findings are sorted; JSON uses
sort_keys; no timestamps or environment-dependent values are emitted, so two
runs on identical input are byte-identical.

## Limitations

- Matcher heuristics only: synonym rewording evades dropped-clause detection,
  and only AC rows plus obligation-keyword lines are extracted.
- Qualifiers are case-insensitive and same-line; the qualifier list may miss a
  case (use `--allow-sha`).
- The cell-level exemption applies only when a table cell is exactly one token.
- Bodies are parsed as text, never executed.
- Flagging aid only; it is not a substitute for review.
- No `.github/` workflow wiring was added for this tool (owner constraint), so
  its unit tests are not yet run by the fixed `tools-tests` CI suites; run them
  locally with the command below until an owner decision permits wiring.

## Tests

    python -m unittest discover -s tools/plan_preservation/tests -p 'test_*.py' -v

The suite includes the measured fixtures F-A, F-B (constructed header-edit),
F-B0 (real page-table control) and F-C (full retained r2 body), the 12 batch-26
dropped substrings across rows R1-R7, size-cap and CLI exit tests, JSON and
determinism checks, and the AC6 static hygiene check.

## Static hygiene allowlist (mirrored for the AC6 check)

The linter imports only: argparse, ast, dataclasses, enum, hashlib, json,
pathlib, re, sys, typing, unicodedata, unittest (the module itself currently
uses the subset argparse, json, re, sys, unicodedata, pathlib, typing). The
static test walks the import tree, asserts this allowlist, and greps both
source files for banned process/network tokens.
