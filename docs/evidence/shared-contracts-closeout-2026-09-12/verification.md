# Shared contracts: implementation verification

> **Current reading, checked 2026-09-24:** This is the initial candidate
> checkpoint for pull request (PR) #90. That change later merged; see the
> [delivery record](README.md). The corrected verification below supersedes
> these initial results. The submission and merge steps at the end describe
> what remained on September 12, not a current permission requirement.

Reading key: Behavioral Eval Runner (BER); Portable Operating System Interface
(POSIX), meaning the Unix-like test environment here; software development kit
(SDK); 256-bit Secure Hash Algorithm 2 digest (SHA-256); architecture decision
record (ADR). An ATX heading is a Markdown heading beginning with `#`.

The [corrected-revision verification](corrected-verification.md) supersedes this
initial candidate record after GitHub review found two additional issues. It
records 987 passing BER tests on each platform and 113 acceptance cases on the
corrected implementation. The initial evidence below remains preserved.

Recorded 2026-09-12. The implementation is committed at
`ffcbb2a47d0e1a32578c5a5ae226e80a908d49bb`, tree
`344a51dbceec528f8223e47e38a8f08e8b0f913c`. The subsequent evidence commit only adds
this record and its attachments. Hosted checks and the final submitted SHA belong
in the PR record, avoiding a self-referential evidence-commit loop.

## Exact source and commands

Full Windows and POSIX checks ran on clean commit
`61f2a4648dead20a7db557441a65dbfd4c1c045a`, tree
`7ec828f7b88d0ba8d800e4a5b703b8716e8382af`. Commit `ffcbb2a` then added the final
empty-heading rejection and two acceptance cases, plus its matching limitation
documentation. The full BER, skill and audit sources are identical between these
commits: `git diff --quiet 61f2a46..ffcbb2a -- tools .claude scripts/tests
scripts/audit-skill-contracts.py` exited zero. The 113-case acceptance suite ran on
clean `ffcbb2a`. This does not claim the complete BER suite reran on that later SHA.

| Check | Windows | POSIX |
| --- | --- | --- |
| Runtime | Python 3.14.7; OpenAI SDK 3.0.0 | Python 3.12.3; SDK absent |
| Validator self-tests | 91 assertions passed | 91 assertions passed |
| Skill validator | 184 valid; zero warnings | 184 valid; zero warnings |
| Contract-audit self-tests | 63 assertions passed | 69 assertions passed |
| BER self-check | 21 checks passed; live dispatch disabled | 21 checks passed; live dispatch disabled |
| Full BER suite at `61f2a46` | 985 tests; 14 skips; zero failures/errors | 985 tests; 13 skips; zero failures/errors |
| Scenario A acceptance | 111 cases at `61f2a46`; **113 at `ffcbb2a`**, PowerShell 5.1 | Not run locally |

Windows BER took 182.884 seconds of test time; POSIX BER took 28.691 seconds.
The [Windows command/result index](logs/windows-61f2a46-results.json) names all
eight commands and their raw logs, each with exit zero. The
[POSIX command/result record](logs/61f2a46-posix.json) binds the source commit and
container image. The container used user `65534:65534`, a read-only source mount
and `--network none`. Windows uses mocked transports with no real provider calls;
the eight SDK-dependent cases execute there. Platform and missing-SDK skips
remain explicit in the raw logs. Local POSIX results do not substitute for hosted
Python 3.14 or PowerShell Core coverage.

Final acceptance output is preserved in
[acceptance-reviewed-head.log](logs/acceptance-reviewed-head.log). The
[source identity evidence](logs/source-identity.txt) records commit trees and the
complete three-file diff from the full-suite revision to the acceptance revision.
[SHA-256 manifest](logs/sha256.json) fingerprints the attached evidence files;
it is an integrity index, not an independent signature or provenance service.
The log directory disables Git text normalization and whitespace linting to
preserve original CRLF and tool-output bytes when cloned on another platform.
Source and documentation outside that raw-log directory retain whitespace checks.

The first uncommitted full Windows run reported one failure in
`test_plan_schema_is_bound_and_key_complete`: it assumed every schema field was
required after an optional trusted lifecycle version was introduced. The fix
retains exact schema parity by asserting required and optional keys separately.
That original [failed log](logs/windows-working-5.log) and
[command/result record](logs/windows-working-results.json) remain available.
The subsequent focused 32-case run and full committed run passed. The earlier
working-run result index references preliminary logs retained locally; the failed
full-suite log is the preliminary attachment preserved here.

## Independent read-only review

The owner has standing permission for read-only agents. Three agents reviewed
distinct bounded slices using Aegis library, contract and QA review workflows:

- Core contracts: the approval register, orchestrator, both roadmap skills and
  skill-quality reviewer were approved after their workflows, references and
  evals agreed on lifecycle history, actual commitment and existing authority.
- Execution and draft contracts: all nine manual routes and five draft authors
  were approved after two remaining ADR/output wording issues were repaired.
  The collision sweep compared all 184 parsed descriptions against 19 changed
  jobs (11 changed descriptions), finding no new ownership/trigger collision.
- Code and acceptance: the reviewer approved exact `ffcbb2a`, tree
  `344a51dbceec528f8223e47e38a8f08e8b0f913c`, conditional on the final acceptance
  suite. That suite then passed all 113 cases. Review-discovered Markdown parser
  bypasses were repaired and covered by negative cases, including the last empty
  ATX-heading case.

These are local AI reviews. They do not satisfy GitHub's required approving review
and do not measure model trigger accuracy. Authored skill evals are fixtures, not
executed live-model evaluations. Neither measured calibration nor human labels,
holdout execution, OD-1 or WP-2B-4 is completed by these checks.

## Submission and merge boundary

The PR modifies `scripts/tests/test_validator.py` and
`scripts/tests/test_audit_skill_contracts.py`. The current workflow intentionally
fails `gate-guard` when `scripts/tests/` changes and prints that manual review and
merge are required. The required approving-review count is also one. Normal
merge will be attempted after hosted validation; any administrator merge needs
specific owner authorization for the concrete PR revision. PR #88's administrator
authorization is not transferred to this PR. No workflow or protection setting
is weakened here.
