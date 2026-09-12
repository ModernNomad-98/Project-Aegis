# Candidate verification — 2026-09-12

Code candidate: `5863fb1ef2fa95f653e7983b74cea16caa95555b`.
Tree: `88f04538a9fcfad9e13117c7d8d3afb28dbadfe7`.

The following completed checks cover the code candidate reviewed in
[reviews.md](reviews.md). This evidence-only follow-up commit does not change
runtime, tests, configuration or skills. The PR body records the final submitted
head and its check results; adding this record does not silently relabel an
earlier run as a test of a later commit.

| Check | Actual result |
| --- | --- |
| Windows / Python 3.14.7 / OpenAI SDK 3.0.0 | 969 tests; zero failures/errors; 14 skips; 196.094 seconds test time |
| POSIX / Python 3.12.3 / network-disabled container | 969 tests; zero failures/errors; 13 skips; 31.484 seconds test time |
| Validator self-tests / Python 3.14.7, PyYAML 6.0.3 | 91 assertions passed |
| Skill validation | 184 valid skills; zero warnings |
| Contract-audit self-tests, including PR #89 | 62 assertions passed |
| Runner self-check | 21 checks PASS; generic live dispatch DISABLED |
| DCO, `origin/main..HEAD` | All 13 non-merge commits signed off or exempt |
| Complete proposal whitespace | `git diff --check origin/main...HEAD` passed |
| Protected enforcement paths against main | No changes |
| Independent execution/security/code and QA review | Both approve scoped engineering; no remaining substantiated defect found |

## Commands and environment

The Windows command was:

```text
<isolated-SDK-python> -B -m unittest discover -s tools/behavioral_eval_runner/tests -p test_*.py -v
```

It ran as the checkout owner with process-local
`TEMP=TMP=C:\Users\PETERN~1\AppData\Local\Temp` and
`PYTHONDONTWRITEBYTECODE=1`, preserving actual short-path exposure. The same
environment's system Python ran the validators, self-check and DCO command.
The six transport SDK-configuration tests and two SDK deadline/cancellation
tests all executed. Both new Windows-specific regressions executed, with no
alias-availability skip. The junction fallback test also passed.

POSIX used the already available image
`sha256:9bd26ad900bb5e0f4dee75839e957a89ae89c2b7ab1e76050e559790e946b948`,
`--init`, `--pull never`, `--network none`, UID/GID `65534:65534`, and a read-only
source mount. The helper copied Git metadata to a disposable container directory
and checked out the full candidate SHA before running the same unittest command.
The empty-area swap test executed and passed.

## Preserved logs and limitations

[Windows and gate metadata](verification/pr88-5863fb1-results.json) references
`pr88-5863fb1-0.log` through `-6.log` in the same directory. The full
[Windows suite log](verification/pr88-5863fb1-6.log),
[POSIX metadata](verification/pr88-5863fb1-posix.json),
[POSIX suite log](verification/pr88-5863fb1-posix.log), and executed POSIX
helpers are committed with this record. Original local path strings identify
where execution occurred; preserved filenames make the evidence available in GitHub.

Windows skips are the declared POSIX-only cases and cases requiring symlink
creation privileges unavailable to this user. POSIX skips comprise eight tests
requiring the pinned SDK, four Windows-only cases, and the existing evidence
writer capability-gated parent-swap test. The materializer's POSIX no-follow
regressions did execute. A pre-existing nonfatal `ResourceWarning` for an unclosed
test pipe appeared in POSIX descendant cleanup, as in the retained preflight.
No threshold or skip condition was relaxed to obtain these results.

These platform runs are complementary. The POSIX interpreter differs from the
GitHub workflow's Python 3.14, and its SDK tests did not execute. GitHub's current
workflow does not run either BER or contract-audit tests; its green status alone
cannot establish these results. Windows detection-only race limitations and
restricted-sandbox process-control limitations remain explicit.

All inputs were synthetic and all provider interactions were fake or mocked:
zero live provider calls, no real credentials and no measured calibration claim.
The missing approved input bytes, replacement preparation, human label decision,
holdout execution, measured acceptance, OD-1 and required GitHub approval remain
separate dependencies. PR #88 engineering closure does not mark WP-2B-3 DONE.
