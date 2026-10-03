# Process issues and prevention — issue register, 2026-10-02

> **Current reading, checked 2026-10-02:** this page records six defect classes
> that one coordinated documentation session observed, each with the command
> that proves it and the standing rule that prevents it. It is a **working
> rule** for agents, not a narrative and not a status report. Every evidence
> claim was re-run against the clean mirror `C:\src\Project Aegis\coord-main`
> at `origin/main` = `6715cefc9347ec0c5e3bd93b65f580f0d7545d3f` on 2026-10-02,
> and the pull request (PR) timestamps were re-read from the GitHub API on the
> same day. Claims that could not be verified from this repository are labelled
> **UNVERIFIED** where they appear, not omitted.

**Terms:** a **base SHA** is the revision a ledger row names as a page's last
recorded acceptance. A **dangling object** is a commit that still exists in one
repository's object store but that no branch, tag or other ref reaches. A
**review record** here means a posted comment that binds a verdict to one head
revision, which is this repository's established substitute for a formal
GitHub review object. **Codex** is the external review bot; **AEGIS-APR-050**
is the owner approval register entry that governs whether its unavailability is
confirmed at a given head. **Continuous integration (CI)** runs the automated
checks. **gate-guard** is the required check that fails a PR touching the merge
gate and its enforcement surfaces. **Head** is the commit a PR currently
proposes for merge.

## How to use this document

This page is read in two situations.

1. **Before dispatching or performing staged work.** Read the rule you are
   about to rely on and run its **Detection check** yourself, in the same turn,
   against the revision you are acting on. The six rules carry stable IDs
   (`PROC-01` … `PROC-06`) so a brief, a review record or a PR description can
   cite one without restating it.
2. **After a defect is found.** Add a class here using the same five-part shape:
   **Issue / Evidence / How it happened / Standing rule / Detection check**. Do
   not record a class whose evidence you could not reproduce; record the
   corrected version instead, and say which part failed.

The shape is deliberate. "Evidence" is a command and its observed output, so a
later reader re-runs it rather than trusting this page. "Standing rule" is
phrased as an action an agent takes, not as a value it holds. "Detection check"
is a command or a concrete verification step, so compliance is observable.

A rule recorded here is not a behaviour change. Under
[`AGENTS.md`](../../../AGENTS.md), a rule holds only when it is executed as
commands at the moment of reporting, not recalled as an intention.

---

## Class 1 — a reachability claim that is true in a mirror and false in a fresh clone

### Issue

The documentation readability ledger on `main` asserts, at the
[documentation readability backlog](../../roadmaps/aegis-documentation-readability-backlog.md)
lines 2790–2791:

> Each base SHA is the page's last recorded acceptance and is an ancestor of
> `origin/main`

The claim is **false for one of the ten rows it covers**. The row at line 2786,
for `cloud-security-baseline-reviewer/SKILL.md`, names base
`65bacc7d6b85` — a pre-rebase commit that no ref reaches and that a fresh clone
would not contain. **This false sentence is on `main` now.** Its correction is
owed and is deliberately not written by this page's PR (see "Owed work").

### Evidence

All commands run in `C:\src\Project Aegis\coord-main`. **PROVEN.**

```text
$ git merge-base --is-ancestor 65bacc7d6b85 origin/main ; echo $?
1
$ git merge-base --is-ancestor 65bacc7d6b85 6715cefc9347ec0c5e3bd93b65f580f0d7545d3f ; echo $?
1
$ git rev-list --all | grep -c '^65bacc7d6b85'
0                      # ABSENT from all 1882 commits reachable from every ref
$ git cat-file -t 65bacc7d6b85
commit                 # ...yet the object RESOLVES in this mirror
$ git for-each-ref --contains 65bacc7d6b85 --format='%(refname)'
                       # no output: NO ref contains it
```

The fifth command is the load-bearing one: the object *exists* and `cat-file`
*resolves* it, while no ref reaches it. A verifier who stops at "the SHA
resolves" concludes the row reproduces. It does not reproduce from a clean
clone.

Resolving a **prefix** is even weaker evidence, and the two commands disagree:

```text
$ git rev-parse 65bacc7d6b85
65bacc7d6b854205cf8bdcc7a1a58f8ef76dc6c7
$ git rev-parse 65bacc7
65bacc7d6b854205cf8bdcc7a1a58f8ef76dc6c7
$ git cat-file -t 65bacc3 ; echo $?
fatal: Not a valid object name 65bacc3
128
```

**Provenance of the false sentence.** It entered with PR #626's squash commit
`bff75d9c`, not with any earlier revision. **PROVEN.**

```text
$ git log --format='%H %cI %s' -S "Each base SHA is the page's last recorded acceptance" \
    origin/main -- docs/roadmaps/aegis-documentation-readability-backlog.md
bff75d9c556009cb0c51dbedaaa97a90d55f4ef8 2026-10-02T17:10:41-07:00 \
  docs(roadmaps): correct the readability backlog's pending floor to 35 (#626)
```

The sentence is present at PR #626's reviewed head `1e8b81e7` and absent at that
head's parent, so it is that PR's own content rather than inherited text.

**A second instance of the same confusion, proven on the same PR.** PR #626's
reviewed head is itself unreachable from `main`, because the PR was
squash-merged:

```text
$ git merge-base --is-ancestor 1e8b81e74b4d64ce86884807df4bee4ee557c208 origin/main ; echo $?
1
```

`1e8b81e7` was the reviewed head, is the `headRefOid` recorded on PR #626, and
is **not** a commit on `main`; the content landed as `bff75d9c`. So
"the head is an ancestor of main" is not a valid test after a squash merge
either, and a check built on it produces a false negative on correct work. The
valid question is always whether the **content** is on `main`.

### How it happened

A branch in the shared mirror was rebased. Rebasing leaves the pre-rebase
commits in the object store, where they keep resolving for `cat-file`,
`rev-parse` and `log <sha>` long after every ref has moved away from them. Work
was then verified against that mirror rather than against a fresh clone, so the
row's base SHA resolved, the row's figures reproduced, and the accompanying
sentence "each base SHA … is an ancestor of `origin/main`" was written as
though the resolution had established reachability. It had not. Resolution
proves the bytes exist in **this** object store; reachability is a property of
the ref graph, and the two come apart exactly in a repository that has been
rebased.

The failure is silent in the direction that matters. In a fresh clone the
command that would expose it (`git cat-file -t`) is the one that fails, so a
fresh-clone verifier sees an error where the mirror verifier saw a commit, and
the two disagree about the *evidence* rather than about the *conclusion*.

### Standing rule — `PROC-01`

**A claim that a revision is reachable must be verified by an explicit
reachability test against the ref graph, never by the mere resolution of the
object.** Use `git merge-base --is-ancestor <sha> <ref>` (exit 0 means
ancestor) and `git for-each-ref --contains <sha>` (a ref name, or nothing).
`git cat-file -t <sha>`, `git rev-parse <sha>`, a resolving prefix and a
successful `git diff <sha> <ref> -- <path>` are **evidence of nothing** about
reachability. Where the claim will be read by someone else, verify it against a
**fresh clone** of the default branch, or state the test you ran and its exit
status. Where a squash or rebase merge is in play, do not test the head at all:
test whether the reviewed **content** is present on the default branch.

### Detection check

```text
$ git merge-base --is-ancestor <sha> origin/main ; echo $?
```

Exit `0` = the claim may stand. Exit `1` = the claim is false for that row, and
the text asserting it must be corrected or the row must carry the caveat. Before
publishing any sentence of the form "is an ancestor of", "is on `main`" or "is
in `rev-list`", run this for **every** SHA the sentence covers, and count them:

```text
$ git for-each-ref --contains <sha> --format='%(refname)' | wc -l
```

`0` means no ref reaches it. Do not record a reachability claim whose SHAs you
have not run this against, one by one.

---

## Class 2 — merge before the review record exists

### Issue

The repository's stage order requires that a merge happen only after review
passes at the exact head being merged
([`AGENTS.md`](../../../AGENTS.md) line 64 onward). In this session **two pull
requests merged with no review record in existence at merge time**, and a third
merged correctly, so the defect is intermittent and therefore easy to miss.

### Evidence

Read from the GitHub API on 2026-10-02. **PROVEN.**

```text
$ gh pr view <n> --repo ModernNomad-98/Project-Aegis --json mergedAt,headRefOid,comments
```

| PR | merged at (UTC) | review records posted (UTC) | review existed at merge? |
| --- | --- | --- | --- |
| #623 | 2026-10-03T00:01:15Z | 23:59:41, 23:59:54, 00:00:08, 00:00:39, 00:00:41, 00:00:42 | **Yes** — all six precede the merge |
| #626 | 2026-10-03T00:10:41Z | 00:11:52, 00:13:01 | **No** — first record 71 s *after* the merge |
| #627 | 2026-10-03T00:10:55Z | 00:13:11, 00:13:13 | **No** — first record 136 s *after* the merge |

**Correction to the session's own record of #623.** The reported finding named
three records; the API returns **six** review records before `mergedAt`, plus a
Codex notice at 23:54:19Z, for seven comments preceding the merge. The
conclusion ("records preceded the merge") is correct and the correction makes it
stronger; the count was understated. Counting records by reading a summary is
how that happens, which is why the rule below counts with a command.

#626 and #627 merged **14 seconds apart**, and #624 merged at 00:11:39Z, so
three merges landed inside 58 seconds. That is the signature of a batch merge
dispatch issued while review of the same PRs was still running.

**The honest limit of a post-merge review record.** A record posted after the
merge is not worthless: it still reads the change and can still find defects.
What it cannot do is gate. PR #626's post-merge record returned **FIX-FIRST**
and correctly identified the Class 1 defect — a real, reproduced falsehood in
the text that had just been merged:

```text
### NOT reproduced (PROVEN FALSE) — the reason for the verdict
The note asserts: "Each base SHA is the page's last recorded acceptance and
**is an ancestor of `origin/main`**."
...
**VERDICT: FIX-FIRST.** Not merged at this head.
```

That is precisely the finding a pre-merge gate would have stopped. Instead the
false sentence entered `main` and its correction is now owed as follow-up work.
A report that presents such a record as evidence that review gatekept the merge
is misleading, however accurate the record itself is.

### How it happened

The coordinator dispatched a **MERGE agent and a REVIEW agent on the same pull
request concurrently**. The stages are meant to be sequential and to be
performed by different agents, and two agents holding one PR race: the merge
can reach the remote first, and when it does, the review is demoted from a gate
to a post-mortem without anyone deciding that. Nothing in the repository detects
the race, because both agents act correctly on the state each one observed.

The cadence log records the coordinator hitting the runtime's active-child
limit at this time (`.coord/coordinator-cadence.jsonl`, entry
`2026-10-02T17:01:00-07:00`: `idle: 0`, `running: 15`), which is the pressure
under which concurrent dispatch on one PR becomes tempting.

### Standing rule — `PROC-02`

**Do not dispatch a merge until a review record bound to the CURRENT head is
already posted, and the dispatcher has verified that binding itself; and never
let two agents hold the same pull request at the same time.** The merge agent
re-verifies the binding at the moment it acts rather than trusting the brief
(see `PROC-03`). A review record whose verdict is bound to an earlier head does
not satisfy this rule: a moved head voids it.

### Detection check

Run **before** dispatching the merge, and again in the merge agent's own turn,
ten seconds before merging:

```text
$ gh pr view <n> --repo ModernNomad-98/Project-Aegis --json headRefOid,mergedAt
$ gh pr view <n> --repo ModernNomad-98/Project-Aegis --json comments \
    --template '{{range .comments}}{{.createdAt}} {{.author.login}}{{"\n"}}{{end}}'
```

Three conditions, all of which must hold:

1. At least one comment timestamp is **earlier than now**, and its body names
   the same head SHA that `headRefOid` reports. The head SHA in the record is
   the binding: compare the two strings, do not compare verdicts.
2. No commit has been pushed to the branch since that record's timestamp.
3. No merge agent is currently dispatched on this PR, and no review agent is
   currently dispatched on it either, unless the merge agent is waiting on that
   review. Concurrency on one PR is the defect.

For the after-the-fact version, compare `mergedAt` against the **earliest**
comment timestamp whose body contains a verdict:

```text
$ gh pr view <n> --repo ModernNomad-98/Project-Aegis --json mergedAt,comments
```

If `mergedAt` precedes the earliest review-record timestamp, that merge gated
nothing. This detector is diagnostic only — it runs after the merge and cannot
prevent one.

---

## Class 3 — a briefing that is stale or incomplete, and the failure it nearly caused

### Issue

A brief asserted that a gate condition was unmet, an independent reviewer
measured the condition at one instant and agreed, and a qualifying artifact
arrived **11 seconds after that measurement** — satisfying the condition before
the merge it was said to block. The reviewer's conclusion was **stale, not
wrong**.

### Evidence

Read from the GitHub API on 2026-10-02. **PROVEN.**

```text
$ gh pr view 624 --repo ModernNomad-98/Project-Aegis --json mergedAt,headRefOid
mergedAt   = 2026-10-03T00:11:39Z
headRefOid = a06344226bfe777a5009a69b079283c2577d9570
$ git log -1 --format='%cI' a0634422
2026-10-02T17:04:58-07:00        # = 2026-10-03T00:04:58Z, the head's own instant
```

PR #624 carries **three** Codex notices, not one:

| # | posted (UTC) | relation to the head's own instant (00:04:58Z) |
| --- | --- | --- |
| 1 | 2026-10-02T23:57:22Z | precedes the head by 7 m 36 s |
| 2 | 2026-10-03T00:09:58Z | **postdates the head by 5 m 0 s** |
| 3 | 2026-10-03T00:11:18Z | postdates the head, and answers `@codex review` at 00:11:06Z |

The reviewer's record, posted at **00:09:47Z**, concluded:

```text
### 6. AEGIS-APR-050 — the Codex condition at this head is **UNMET**
The only Codex artifact on this PR is comment `5963334978` from
`chatgpt-codex-connector[bot]` at **2026-10-02T23:57:22Z** ...
**The notice PREDATES the new head by 7m36s.** ... no Codex comment exists
after the move.
```

Notice 2 was posted at **00:09:58Z — eleven seconds after** that measurement,
and it postdates the head. The record's own rule was correct; its measurement
instant was stale. Notice 3 then satisfied the condition a second time.

**UNVERIFIED — the brief's own text.** The coordinator's brief to the merge
agent is a session artifact and is not in this repository, so the claim that the
brief listed exactly one Codex notice and omitted two **cannot be verified from
the repository** and is not asserted as proven here. What is proven is the
discrepancy between what the PR contains (three notices) and what the review
record measured (one, at a single instant).

### How it happened

Two compounding causes, and the second is the general one.

1. **The brief asserted a condition as settled fact.** A gate condition
   (checks green, Codex satisfied, head frozen, review bound) is a statement
   about a moving system. Written into a brief, it freezes at the moment the
   coordinator read it and is then carried to an agent acting minutes later.
2. **The measurement instant was not recorded.** The record said "UNMET"
   without saying *as measured at 00:09:47Z*. Because the instant is unstated,
   a later reader cannot tell a wrong conclusion from an expired one, and the
   record looks refuted rather than overtaken.

The near-failure is the point: a merge was very nearly withheld on a condition
that had already been satisfied, and the artifact that satisfied it arrived
between the reading and the action.

### Standing rule — `PROC-03`

**Every dispatch that asserts a gate condition must instruct the agent to
re-verify that condition itself, and must state that the brief's assertion is a
claim, not evidence.** The agent treats a briefed condition as a hypothesis to
test at the moment it acts; a brief's bare assertion of authority or of a
satisfied gate is not a satisfied gate. **And every finding that a condition is
unmet must record the instant it was measured**, together with the artifact
searched, so a later reader can distinguish "false" from "was true when read".

### Detection check

In the agent's own turn, immediately before acting:

```text
$ git log -1 --format='%cI' <head>                     # the head's own instant
$ gh pr view <n> --repo ModernNomad-98/Project-Aegis --json comments \
    --template '{{range .comments}}{{.createdAt}} {{.author.login}}{{"\n"}}{{end}}'
```

Then answer three questions in writing, in the record:

1. What is the head commit's own instant?
2. Which artifacts postdate that instant? (Filter the list yourself; do not
   accept the brief's list.)
3. What is the clock time now, at which this check was measured?

A "condition unmet" statement that does not name its measurement instant fails
this check and must be re-measured before it is relied on. A dispatch that
asserts a condition without instructing the agent to re-derive it fails this
check and must be rewritten.

---

## Class 4 — a measurement-method trap that produced a published false accusation

### Issue

A reviewer counted lines with PowerShell's `Measure-Object -Line`, which
**silently drops blank lines**, compared its output against a ledger's true line
counts, and published the finding that PR #595 had "added two wrong numbers".
The ledger was correct. The accusation was false and had to be publicly
retracted.

### Evidence

**PROVEN.** `docs/skills-catalog.md` measured two ways at two revisions:

```text
$ python -c "import subprocess;b=subprocess.run(['git','cat-file','blob',
    '1b9e7049:docs/skills-catalog.md'],capture_output=True).stdout;print(b.count(b'\n'))"
1492                    # the newline count: the 0x0A bytes in the raw blob
$ git show 1b9e7049:docs/skills-catalog.md | Measure-Object -Line
1319                    # non-blank lines only (the forbidden method, shown to expose the trap)
                         # 1492 − 1319 = 173 blank lines
$ python -c "import subprocess;b=subprocess.run(['git','cat-file','blob',
    '93c0834f:docs/skills-catalog.md'],capture_output=True).stdout;print(b.count(b'\n'))"
1504                    # the newline count: the 0x0A bytes in the raw blob
$ git show 93c0834f:docs/skills-catalog.md | Measure-Object -Line
1331                    # non-blank lines only (the forbidden method, shown to expose the trap)
                         # 1504 − 1331 = 173 blank lines
```

The identity `1504 − 173 = 1331` (and `1492 − 173 = 1319`) is the whole
finding: the two "wrong numbers" in the accusation are exactly the *non-blank*
counts of a file whose *line* counts the ledger reported correctly. The offset
is a near-constant 173 because prose edits do not change the blank-line count,
which is what makes the trap dangerous — the wrong method is self-consistent
from revision to revision, so comparing two of its outputs looks sound.

The published accusation and its retraction, both re-read from the API:

```text
$ gh api repos/ModernNomad-98/Project-Aegis/issues/comments/5963257423
created_at = 2026-10-02T23:48:39Z   # "APPROVE WITH A FINDING" — the false accusation
$ gh api repos/ModernNomad-98/Project-Aegis/issues/comments/5963289254
created_at = 2026-10-02T23:52:18Z   # "the finding ... is FALSE and is withdrawn"
```

The accusation is [PR #595 comment
5963257423](https://github.com/ModernNomad-98/Project-Aegis/pull/595#issuecomment-5963257423)
and the retraction is [PR #595 comment
5963289254](https://github.com/ModernNomad-98/Project-Aegis/pull/595#issuecomment-5963289254).
The retraction is correct and is itself an instance of the rule below: it names
its counting method for every figure.

**The trailing-newline trap, proved on a real file.** A `git show` pipeline
decodes the blob into an array of lines and **discards the information about
whether the final line was terminated**. Both the element count and the
join-and-split form built on that array therefore report *lines*, not
newlines, and **over-report by exactly 1 when the final line has no newline**.
Measured at `6715cefc`, where 32 of 1426 tracked blobs are unterminated:

```text
$ f=artifacts/evidence/behavioral-eval-runner-wp-2b-0-finalization.json
$c = git show 6715cefc:$f      # an array of lines: the terminator is lost on this line
$ ($c | Measure-Object).Count                              # 13  — lines, not newlines
$ (($c -join "`n").Split("`n")).Count                       # 13  — the same array joined and re-split
$ python -c "import subprocess;b=subprocess.run(['git','cat-file','blob',
    '6715cefc:'+'$f'],capture_output=True).stdout;print(b.count(b'\n'))"
12                                                          # the true newline count
$ ... b.endswith(b'\n')                                     # False
```

**CORRECTION to the session's own earlier analysis.** The scratch note that
first documented this trap recommends
`(($c -join "`n").Split("`n")).Count` as "the correct method (newline count)".
That is wrong, and this page records the corrected version: the join-and-split
form counts **array elements**, so it over-reports by 1 on an unterminated final
line exactly as the element count does. On the two revisions above it happens to
agree with the true count only because both blobs are newline-terminated —
`git cat-file -s 93c0834f:docs/skills-catalog.md` is 160920 bytes containing
1504 `0x0A` bytes, and `endswith(b'\n')` is `True`. The only method that truly
counts newlines is **counting `0x0A` bytes in the raw blob**, or an equivalent
newline-counting form that sees the final unterminated line.

The scratch note also cited the offset as 173 and the two pairs as
1492/1319 and 1504/1331; those figures reproduce exactly. What does not
reproduce is its recommended method. The note is session scratch at
`C:\src\Project Aegis\coord-main\artifacts\coord\line-count-trap.md`, is not
tracked in this repository, and is not gitignored there.

### How it happened

Two plausible commands over the same input disagree by 173 lines, and the
disagreement is invisible unless you already know that `Measure-Object -Line`
skips blanks. The count was then published next to a count produced by a
different method, and the difference between the methods was reported as an
error in the document. There is no warning, no error and no visual cue: the
number looks like a line count.

### Standing rule — `PROC-04`

**Every published line count must name the counting method; a line count must
be a newline count; `Measure-Object -Line` is forbidden for line counts; and a
trailing-newline change must be checked explicitly.** Concretely: state whether
a figure is a file's length (newline count) or a change size (added + deleted,
or net, from `git diff --numstat`); never place a non-blank count beside a line
count; never compare counts produced by two different methods without saying so;
and before publishing, reproduce the figure by a **second independent route**
(for a length, the summed `numstat` chain from a known-good base). Where the
figure describes a change, take it from a commit's own parent→commit diff or a
genuine ancestor range — never a two-dot diff between unrelated tips.

### Detection check

```text
$ python -c "import subprocess;b=subprocess.run(['git','cat-file','blob',
    'REV:PATH'],capture_output=True).stdout;print(b.count(b'\n'), b.endswith(b'\n'))"
```

The first number is the true line count. The second is `False` for the 32
unterminated blobs at `6715cefc` — and for any file that has just lost or gained
a trailing newline, which is exactly when a length-comparison claim goes wrong
by one. To find them repository-wide:

```text
$ git ls-tree -r --name-only <rev> | while read -r f; do
    n=$(git cat-file blob "<rev>:$f" | tail -c1 | od -An -c | tr -d ' \n')
    [ "$n" = '\n' ] || echo "UNTERMINATED $f"
  done
```

To find text that mentions the forbidden method:

```text
$ git grep -n 'Measure-Object -Line' -- '*.md'
```

**This grep is a review prompt, not a gate.** It has hits on `main` today —
`docs/evidence/session-continuation-2026-09-30-evening.md:176`,
`docs/roadmaps/aegis-documentation-readability-backlog.md:2772` and this page —
and **every one of them is text *about* the trap, not a count produced by it**.
So a hit must be read, not failed on. A mechanical version of this check needs
an allowlist of pages that define the rule. Any published count that fails to
name its method fails this check.

---

## Class 5 — acting on an unmerged artifact

### Issue

A tool that lives **inside an open, unmerged, unreviewed pull request** was used
to derive a finding — "159 pages have no review record" — and work was nearly
dispatched from that finding. It was caught before dispatch.

### Evidence

**PROVEN** for the artifact's status; **UNVERIFIED** for the figure.

```text
$ gh pr view 629 --repo ModernNomad-98/Project-Aegis --json state,mergedAt,headRefOid,title
state = OPEN   mergedAt = (empty)   head = 7c52b6f63dc14dd1cb794b486135c2d9eb988302
title = docs(tools): add a per-path readability acceptance index
$ gh pr view 629 --repo ModernNomad-98/Project-Aegis --json files    # 12 files, all under:
tools/readability_acceptance/{README.md,acceptance-index.json,build_index.py,
  check_index.py,investigate_commits.py,scan_lines.py,scan_paragraphs.py,
  scan_rounds.py,scan_stated.py,stated-acceptances.json,verify_ground_truth.py,
  acceptance-verdicts-stage-1.json}
$ git cat-file -e origin/main:tools/readability_acceptance/check_index.py ; echo $?
fatal: path 'tools/readability_acceptance/check_index.py' does not exist in 'origin/main'
128
$ git ls-tree --name-only origin/main tools/
tools/aegis_delivery_control
tools/aegis_setup
tools/behavioral_eval_runner
```

The tool is absent from the default branch, so its output cannot be re-derived
there. **The "159 no-record pages" figure is UNVERIFIED**: re-deriving it would
require running the unmerged tool, which this page's PR does not do and does not
authorize. Anyone acting on that figure must first re-derive it from `main`.

### How it happened

An agent's instrument becomes useful before it becomes reviewed. The tool was
built to answer exactly the question the coordinator had, it worked, and its
output was treated as an established fact about `main` while the code that
produced it was still a proposal. Nothing in the repository distinguishes "a
number produced by a tool on `main`" from "a number produced by a tool in a PR" —
both look like a number.

### Standing rule — `PROC-05`

**No work may be directed from an artifact that is not on the default branch and
independently reviewed.** A provisional artifact may be used **only to
explore**, and any conclusion drawn from it must be **re-derived from `main`**
before it drives a dispatch, a brief, a merge decision or a published claim.
Where the artifact cannot be re-derived from `main`, the conclusion is recorded
as **unverified** and no work is dispatched from it.

### Detection check

Before a figure drives any dispatch, name the path that produced it and ask
whether that path exists on the default branch:

```text
$ git cat-file -e origin/main:<path> ; echo $?
```

Exit `128` with "does not exist in 'origin/main'" means the instrument is not on
the default branch: the figure is provisional. Exit `0` means the path exists —
which is **not** the same as "the figure was re-derived"; still re-run it. To
check whether a figure's source is unmerged without knowing its path:

```text
$ gh pr list --repo ModernNomad-98/Project-Aegis --state open --json number,title,files
```

---

## Class 6 — re-dispatching a lane that was not dead, and the second writer it puts on one worktree

### Issue

The coordinator dispatched the TEN-PAGES lane **twice**. The first dispatch created
the worktree `wt-ten`, its branch and its HEAD at `2026-10-02 17:13:20 -07:00`; the
second was sent later because the coordinator believed the first had produced
nothing. **Both ran.** One attempt committed `4d08377d` at 17:15:13 while the other
was concurrently editing the same files in the same worktree, and five commits landed
on that branch inside seven minutes (17:13:20 to 17:19:48). The second dispatch did
not duplicate work on a dead lane; it added a second writer to a live one.

### Evidence

Run read-only, in `C:\src\Project Aegis\coord-main` and with `git -C` into
`C:\src\Project Aegis\wt-ten`. **PROVEN** except where labelled otherwise. The
reader's own provenance matters here: `coord-main` is **not** a separate clone —
`git rev-parse --git-dir` returns
`C:/src/Project Aegis/Project-Aegis/.git/worktrees/coord-main` — so it shares one
object store and one ref namespace with every lane's worktree, which is why the
commits below resolve here at all. `origin/main` was re-fetched, not assumed:

```text
$ git fetch origin && git rev-parse origin/main
5703e93f1d29cdc382f691f0e9cfecb8d49faa30
```

**Two dispatches, one worktree.** The reflog is the artifact, and it shows six
commits of which five survive:

```text
$ git -C "C:\src\Project Aegis\wt-ten" reflog --date=iso
145647cc HEAD@{2026-10-02 17:19:48 -0700}: commit: fix(skills): restore the seven failure-mode count in rls-policy-auditor
a69d4d1f HEAD@{2026-10-02 17:19:42 -0700}: commit: docs(skills): link the reconciliation citation in rls-policy-auditor
9dd8c59a HEAD@{2026-10-02 17:19:37 -0700}: reset: moving to 9dd8c59a
5ebfee93 HEAD@{2026-10-02 17:19:29 -0700}: commit: docs(skills): link the reconciliation citation in rls-policy-auditor
9dd8c59a HEAD@{2026-10-02 17:19:28 -0700}: commit: docs(skills): define TALI in the local-ci-mirror-preflight reading key
54f2dd02 HEAD@{2026-10-02 17:19:28 -0700}: commit: docs(skills): define TSC and SDLC at first use in compliance-control-foundation
4d08377d HEAD@{2026-10-02 17:15:13 -0700}: commit: docs(skills): correct the rls-policy-auditor failure-mode count
6715cefc HEAD@{2026-10-02 17:13:20 -0700}: reset: moving to HEAD
6715cefc HEAD@{2026-10-02 17:13:19 -0700}:
$ git rev-list --count 6715cefc..145647cc
5
```

`5ebfee93` is the tell: a commit written at 17:19:29 was removed by a
`reset: moving to 9dd8c59a` eight seconds later, and a commit with the same subject
was written again at 17:19:42, thirteen seconds after the first. A commit written,
reset away and rewritten with the same subject inside one worktree is what concurrent
writers look like in a reflog.

**Which agent authored which commit is UNVERIFIED and is not asserted here.** Both
agents commit under one git identity, and commit metadata cannot distinguish them.
The proven cause is narrower and is enough on its own: **the coordinator issued two
dispatches for one lane.**

**The regression those writers left behind, reproduced verbatim.**

```text
$ git show 4d08377d --numstat --format=''
1       1       .claude/skills/rls-policy-auditor/SKILL.md
$ git show 4d08377d --format='' -- .claude/skills/rls-policy-auditor/SKILL.md
-  per-command audit questions, the seven failure-mode catalog with detection
+  per-command audit questions, the eight failure-mode catalog with detection
$ git show 4d08377d:.claude/skills/rls-policy-auditor/references/rls-audit-checklist.md | sed -n 35p
## Seven failure modes (detect → fix)
   numbered items under that heading = 7      # counted, not read off
   failure modes named in Workflow step 4 of SKILL.md = 7
```

The commit message asserts "**eight** distinct failure modes" and then lists
**exactly seven** — missing tenant scope, deny-by-default gap, recursion, unsafe
SECURITY DEFINER, over-broad GRANT, service-role leakage, frontend-derived scope,
counted by splitting the parenthetical. It also claims "the reference itself
enumerates eight numbered modes", and the reference says seven at line 35 with seven
numbered items beneath it. Workflow step 4 names those same seven. **The only place
either file says eight is the edited line itself.** A count word was changed to a
number that no source in the skill supports, by a commit whose own message
contradicts itself one sentence later. That self-contradicting claim, not the
one-word edit, is the durable lesson.

**The briefed claim "the branch was NEVER pushed" has DRIFTED and is now FALSE.**

```text
$ git ls-remote --heads origin | Select-String 'readability-ten-missed-pages'
145647cc9dc74dff259f651442ab7c9c8a14f70a  refs/heads/docs/readability-ten-missed-pages
$ git merge-base --is-ancestor 4d08377d 145647cc ; echo $?
0
$ git for-each-ref --contains 4d08377d --format='%(refname)'
refs/heads/docs/readability-ten-missed-pages
refs/remotes/origin/docs/readability-ten-missed-pages
```

The regression commit is therefore **reachable and published**, not a dangling
object: both tests required by `PROC-01` agree. The never-pushed claim was true when
it was first measured and false by the time it was used, because the owning lane
pushed during the same session — so the brief carried a stale measurement forward
without its instant, which is the Class 3 defect. **This is the register's own
subject turning on the register: evidence drifts between measurement and use.** The
drift did no harm here only because it moved the fact from "unpublished" to
"published"; the same mechanism moved Class 3's gate condition the other way.

**The briefed owed item is DISCHARGED by the owning lane, not owed.** The instruction
"the seven→eight regression must be corrected before that branch is pushed" was
already satisfied at `145647cc`, whose subject is exactly that correction:

```text
$ git show 145647cc:.claude/skills/rls-policy-auditor/SKILL.md | sed -n 217p
  per-command audit questions, the seven failure-mode catalog with detection
$ git show origin/main:.claude/skills/rls-policy-auditor/SKILL.md | sed -n 217p
  per-command audit questions, the seven failure-mode catalog with detection
```

**The line is identical; the file is not.** The blobs differ — `cf8d207f` at
`145647cc` against `3d25584f` on `origin/main` — because the branch also carries
`a69d4d1f`'s reconciliation citation. A verifier comparing whole-file hashes would
report a false mismatch, and the count that had to match does match. This is
`PROC-01`'s lesson in miniature: run the test that answers the question asked, and do
not let a broader test answer a narrower one.

**A second instance of the defect, and in this one the rule WORKED.** A later agent
was dispatched for **this** register lane after the lane already existed. Its
`git worktree add` failed with exit 255 — "a branch named
'docs/process-issues-and-prevention' already exists" — and it **self-halted instead
of adding a second writer**. The event is **UNVERIFIED** from this repository: a
failed dispatch leaves no ref, no file and no log entry, and the coordinator's
cadence log `.coord/coordinator-cadence.jsonl` records no such line (read in full,
9 lines). What is proven is the standing condition the failure left and the outcome:

```text
$ git worktree list | Select-String 'wt-register|wt-ten'
C:/src/Project Aegis/wt-register    5520ec4f [docs/process-issues-and-prevention]
C:/src/Project Aegis/wt-ten         145647cc [docs/readability-ten-missed-pages]
```

Exactly one worktree holds each of the two branches. No second writer exists. The
rule worked in the instance where its check had something to see — which is the
distinction the honest limit below turns on.

**A third drift, in this page's own provenance, observed while this class was
written.** The "Current reading" block above cites `origin/main` =
`6715cefc9347ec0c5e3bd93b65f580f0d7545d3f`. Re-fetched while writing this class, it
is `5703e93f1d29cdc382f691f0e9cfecb8d49faa30`. Classes 1–5 were re-checked at the new
revision and still hold: `git merge-base --is-ancestor 65bacc7d6b85 origin/main`
still exits 1, and PR #629 is still `OPEN` with
`git cat-file -e origin/main:tools/readability_acceptance/check_index.py` still
exiting 128. The header is left exactly as written, per this document's practice of
correcting forward rather than rewriting a dated measurement.

**A fourth drift, in the same provenance, observed during the correction pass that answered the independent review of this page, on 2026-10-02.** Re-fetched twice in that pass, `origin/main` returned `f6bf9d9a` and then `d9f57283145ce2608ff76920dddd3db5be48b9a9` — the tip at the time of writing, PR #634, committed `2026-10-02T17:39:36-07:00` — so the `5703e93f` named just above was itself overtaken inside the same session, and the header's `6715cefc` is now four commits behind (`git rev-list --count 6715cefc..origin/main` → 4). Classes 1–5 were re-checked at the newest tip and still hold: `git grep -n "Each base SHA is the page's last recorded acceptance" origin/main -- docs/roadmaps/aegis-documentation-readability-backlog.md` still hits line 2790, `git merge-base --is-ancestor 65bacc7d6b85 origin/main` still exits 1, `git cat-file -e origin/main:tools/readability_acceptance/check_index.py` still exits 128, and PR #629 is still `OPEN`. This note is a dated measurement too, and will drift in turn.

### How it happened

**Root cause: the absence of commits was read as evidence that the lane was dead.**
At the moment of the second dispatch the lane had produced no commits. It was not
dead; it was early, with uncommitted work in flight in its worktree. The coordinator
had one observable — the commit log — and read a negative there as a positive
elsewhere: "no commits" became "no work", and "no work" became "safe to re-dispatch".
Neither inference holds. A lane's first *durable* artifact is usually its first
commit, which arrives after its worktree, its branch and its uncommitted edits, and
in that gap the repository looks the same for a lane that is early and for a lane
that was never dispatched.

**This shares its cause with Class 2.** There, a merge agent and a review agent held
one pull request concurrently, and #626 and #627 merged with no review record in
existence at merge time; here, two agents held one worktree concurrently. Both are
**one resource with two writers**, and in both the coordinator dispatched the second
writer on the strength of a state that did not yet show the first one's effect — a
review record not yet posted, a commit not yet made. `PROC-02` forbids two agents on
one pull request; this class forbids two agents on one worktree, for the same reason.

### Standing rule — `PROC-06`

**Before re-dispatching any lane, verify that the previous attempt is actually
inactive. Absence of commits is NOT evidence of an inactive lane.** The verification
is a positive search for the lane's artifacts, run in the dispatcher's own turn, and
a lane may be re-dispatched only when that search finds **none** of them — or when
the previous attempt has **explicitly reported completion**. A lane whose worktree,
branch, remote ref or pull request exists is live until it says otherwise, however
long its commit log has been empty.

### Detection check

Run all five in the dispatcher's turn, and treat any output other than a refusal to
re-dispatch as a bug:

```text
$ git worktree list
$ git -C <worktree> status --porcelain
$ git branch --list <name>
$ git ls-remote --heads origin <name>
$ gh pr list --head <name> --state all
```

A lane may be re-dispatched only when those five show **no worktree, no local branch,
no remote ref and no pull request**, or when the previous attempt has explicitly
reported completion. A non-empty `status --porcelain` is the strongest signal of all:
it is uncommitted work in flight, which is exactly the state the double dispatch of
Class 6 ran over.

**The honest limit of this rule, which is the load-bearing part.** At the instant of
the original double dispatch this check would have returned **nothing for all five
commands** — there was no worktree, no branch, no remote ref, no PR and no commit for
that lane, because the first dispatch had not yet created them. No check can
distinguish "early" from "dead" in that window; the only defence there is patience,
and **this rule does not solve that case**. What it does solve is the case where a
lane has already left any artifact at all: then the five commands see it and the
second dispatch is refused, as it was for this register's own lane. Saying plainly
which case the rule cannot cover is part of the rule's value, because a rule believed
to cover everything stops the search for the case it misses.

---

## Honest limits of this register

- **It records the defects this session observed.** Six classes were reported. Five
  reproduced by command; the sixth reproduces in its consequence — a published
  regression commit, and a commit written, reset away and rewritten in one worktree —
  while its cause is session state and is labelled UNVERIFIED. There may be others
  that nobody noticed, and an unobserved defect is not covered by any rule here.
  Silence in this document is not evidence of correctness.
- **A rule that is not enforced mechanically can still be forgotten.** `PROC-01`
  through `PROC-06` are written as checks so that compliance is observable, but
  observability is not enforcement: an agent that does not run the check leaves
  no trace that it skipped one. The repository's own cadence log states the
  consequence for its own case — a missing entry means the check did not run,
  not that nothing was wrong.
- **Three of the six classes are dispatch-time properties, and one of them has a
  readable check.** `PROC-02` (no two agents on one PR), the re-verification half of
  `PROC-03` and `PROC-06`'s re-dispatch decision describe what agents were told and
  when; git and GitHub record none of those decisions, so no gate can read them.
  `PROC-06` differs in that the **artifacts a live lane leaves** — worktree, branch,
  remote ref, pull request — *are* readable, which is why it has a command check.
  What stays unreadable is whether a lane that leaves none of them is early rather
  than dead.
- **One class rests on a session artifact that is not in this repository.**
  Class 3's claim about what a brief contained is labelled UNVERIFIED above.
- **One class's cause is session state, and its second instance is a report.**
  Class 6's double dispatch, and the later `git worktree add` that failed and
  self-halted, are dispatch events: a failed dispatch leaves no ref, no file and no
  log entry. Class 6's consequence reproduces in the `wt-ten` reflog and its standing
  condition reproduces in `git worktree list`, but both events are labelled
  UNVERIFIED above.
- **One class's central figure is unverified.** Class 5's "159 pages" figure is
  not reproducible from `main`.
- **This page is itself subject to the same rules.** Its own line count and
  change size are stated with their method in the PR description, and it is
  pending review under the ledger's own rule, since a new page needs a full-page
  read.

## Which rules can be enforced mechanically, and where

`scripts/` is **gate-guard protected**: any pull request touching it fails the
required `gate-guard` check and needs owner-authorised manual review and merge
(see [CONTRIBUTING → External
contributions](../../../CONTRIBUTING.md#external-contributions), and the
[offline CI guide](../../offline-ci.md)). `.github/` is protected the same way.
So every mechanical enforcement below costs a manual-review merge, and none of
it can be added by this PR.

**Mechanically enforceable, and where it would live:**

| Rule | What CI could check | Where it would live |
| --- | --- | --- |
| `PROC-01` | For a declared list of (SHA, claim) pairs in the tracked text, fail when `git merge-base --is-ancestor <sha> origin/main` exits non-zero. Needs a machine-readable list, which does not exist yet. | `scripts/` — gate-guard protected |
| `PROC-04` (forbidden method) | `git grep 'Measure-Object -Line' -- '*.md'` returns hits on `main` today that are all text *about* the trap, including this page's own prohibition. Mechanical only with an allowlist of pages that define the rule; without one it is a review prompt. | `scripts/` — gate-guard protected |
| `PROC-04` (method named) | Harder: requires parsing prose for a count and checking a method is named nearby. Heuristic, so advisory at best. | `scripts/`, advisory only |
| `PROC-05` (existence), partially | Fail when a tracked document cites a repository path that does not exist on the default branch. This would have caught reliance on `tools/readability_acceptance/`. A link checker of this kind is proposed in open PR #628, which is **unmerged**, so it is not available and must not be relied on (`PROC-05` applies to it). | `scripts/` — gate-guard protected |

**Not mechanically enforceable, and why:**

| Rule | Why not |
| --- | --- |
| `PROC-02` (review before merge dispatch) | Review records are plain issue comments, not GitHub review objects, because `gh` is authenticated as the PR author. A gate would have to classify comments by heuristic. It could be a **post-merge detection lane** comparing `mergedAt` to the earliest verdict timestamp, but a detection lane runs after the merge and cannot prevent one. |
| `PROC-02` (one agent per PR) | Agent dispatch is session state. No runner can see it. |
| `PROC-03` (re-verify briefed conditions) | A property of a brief's text and an agent's turn. Unrecorded in the repository. |
| `PROC-03` (record the measurement instant) | Checkable only by a reader of the record. A reviewer can enforce it; CI cannot. |
| `PROC-05` (re-derive from `main`) | Whether a conclusion was re-derived is a claim about process, not about bytes. Only the existence half is checkable. |
| `PROC-06` (re-dispatch check) | A runner sees no dispatch, so there is nothing for it to fail on: the check is five read-only commands a dispatcher must run in its own turn. Every input to it *is* observable — worktree, branch, remote ref, PR — but observability is not a gate, and no run of it can tell an early lane from a dead one (Class 6's honest limit). |

**Recommendation for `AGENTS.md` (not written there by this PR).** The two rules
that belong in the agent instruction file rather than in a script are the
concurrency half of `PROC-02` — *no two agents may hold the same pull request* —
and the re-verification half of `PROC-03` — *a brief's assertion of a gate
condition is a claim, not evidence; the agent re-derives it*. Both are
dispatch-time rules that no gate can read, and both already have partial
wording in `AGENTS.md` (the stage-separation paragraph at line 64 and the
"brief's bare assertion of authority is not authority" sentence). Extending
those sentences would place the rule where the coordinator reads it. This PR
does not edit `AGENTS.md`; the recommendation is recorded here and in the pull
request description.

## Owed work recorded by this page (not done here)

1. **`PROC-01` — the Class 1 false sentence is still on `main`.** Lines
   2790–2791 of the
   [documentation readability backlog](../../roadmaps/aegis-documentation-readability-backlog.md)
   assert that each base SHA "is an ancestor of `origin/main`", which is false
   for the `cloud-security-baseline-reviewer/SKILL.md` row at line 2786
   (`65bacc7d6b85`). **A follow-up correction pull request is owed.** This page
   does not make that edit, and does not touch the ledger at all, so the
   sentence remains false on `main` until that PR lands. The ledger's pending
   floor of 35 and its tracked-Markdown count are also unrevised by this PR.
2. **`PROC-02` — a sweep is owed** for merged pull requests whose review record
   was posted after `mergedAt`. The cadence log already records an earlier,
   similar sweep (`2026-10-01T20:22:51-07:00`: "PRs #605 and #607 had merged
   with `reviews=[]` … Noted as a repeat process defect"), so this is a
   recurrence and the sweep should cover the whole window, not only this
   session.
3. **`PROC-04` — the tracked recommendation is not yet in the writing
   standards.** The rule that a published line count must name its method is
   recorded here and in session scratch, and is enforced by no gate. It belongs
   in the repository's documentation standards, which this PR does not edit.

## Evidence summary

| Class | Claim | Verdict | Command |
| --- | --- | --- | --- |
| 1 | `65bacc7d6b85` is not an ancestor of `origin/main` | **PROVEN** | `git merge-base --is-ancestor 65bacc7d6b85 origin/main` → 1 |
| 1 | The object nonetheless exists in this mirror | **PROVEN** | `git cat-file -t 65bacc7d6b85` → `commit` |
| 1 | No ref reaches it; `rev-list --all` excludes it | **PROVEN** | `git for-each-ref --contains` → empty; `git rev-list --all` → absent |
| 1 | The false sentence entered with PR #626's squash commit `bff75d9c` | **PROVEN** | `git log -S "Each base SHA is the page's last recorded acceptance"` |
| 1 | PR #626's reviewed head `1e8b81e7` is also not on `main` (squash) | **PROVEN** | `git merge-base --is-ancestor 1e8b81e7 origin/main` → 1 |
| 2 | #626 and #627 merged with no review record in existence | **PROVEN** | `gh pr view <n> --json mergedAt,comments` |
| 2 | #623 carried **six** review-record comments before its merge: three named records (audit Audit-1 ACCEPT, readability REMEDY-1 SHIP, security SEC-1 SECURITY-ACCEPT) posted once, twice and three times | **PROVEN** | same |
| 2 | #626's post-merge record returned FIX-FIRST on the Class 1 defect | **PROVEN** | comment body at `2026-10-03T00:13:01Z` |
| 3 | #624's head instant is 00:04:58Z; a Codex notice postdates it at 00:09:58Z | **PROVEN** | `git log -1 --format=%cI a0634422`; `gh pr view 624 --json comments` |
| 3 | The UNMET conclusion was measured at 00:09:47Z, 11 s before that notice | **PROVEN** | comment timestamps |
| 3 | What the coordinator's brief listed | **UNVERIFIED** | brief is a session artifact, not in the repository |
| 4 | True counts are 1492 / 1504; `Measure-Object -Line` gives 1319 / 1331 | **PROVEN** | raw `0x0A` byte count of each blob: `python -c "import subprocess;b=subprocess.run(['git','cat-file','blob','1b9e7049:docs/skills-catalog.md'],capture_output=True).stdout;print(b.count(b'\n'))"` → 1492, the same command at `93c0834f` → 1504; `(git show <rev>:docs/skills-catalog.md \| Measure-Object -Line).Lines` → 1319 / 1331 |
| 4 | The accusation was published and retracted | **PROVEN** | `gh api .../issues/comments/5963257423` and `/5963289254` |
| 4 | The join-and-split method over-reports by 1 on an unterminated blob | **PROVEN** | `behavioral-eval-runner-wp-2b-0-finalization.json`: 13 vs 12 |
| 5 | PR #629 is open and its tool is absent from `main` | **PROVEN** | `gh pr view 629`; `git cat-file -e origin/main:tools/...` → 128 |
| 5 | The "159 no-record pages" figure | **UNVERIFIED** | requires running the unmerged tool; not done |
| 6 | The seven→eight regression reproduces verbatim, and no source supports "eight" | **PROVEN** | `git show 4d08377d --numstat` → `1 1`; `rls-audit-checklist.md:35` = "Seven failure modes"; 7 numbered items; Workflow step 4 names 7 |
| 6 | The briefed "branch was NEVER pushed" is now **false**: the branch is on the remote at `145647cc` | **PROVEN** | `git ls-remote --heads origin`; `git merge-base --is-ancestor 4d08377d 145647cc` → 0; `git for-each-ref --contains 4d08377d` → 2 refs |
| 6 | The seven→eight regression is **discharged** by the owning lane at `145647cc`, not owed | **PROVEN** | line 217 at `145647cc` and at `origin/main` both read "the seven failure-mode catalog" |
| 6 | Two dispatches put two writers on one worktree (`wt-ten`) | **UNVERIFIED** (the dispatch is session state; its consequence reproduces) | `git -C "C:\src\Project Aegis\wt-ten" reflog --date=iso`: 6 commits, one reset away, 5 surviving |
| 6 | A later `git worktree add` failed (exit 255) and the agent self-halted | **UNVERIFIED** (reported in a brief; a failed dispatch leaves no trace) | `git worktree list`: exactly one worktree per branch |

---

**Provenance.** Evidence gathered read-only from the clean mirror
`C:\src\Project Aegis\coord-main` at `origin/main` =
`6715cefc9347ec0c5e3bd93b65f580f0d7545d3f`, plus the GitHub API as
`ModernNomad-98`, on 2026-10-02. Nothing was measured from the stale root
checkout. No provider or model call was made. The cited PR instants fall on
2026-10-03 in Coordinated Universal Time (UTC) while the session's local date is
2026-10-02, which is why this page is dated 2026-10-02 and its table columns are
labelled UTC; the cadence log uses the same local-offset convention. Every line
count in this page is a **newline count**, being the number of `0x0A` bytes in
the raw blob; every change size is from `git diff --numstat` and is stated as
added + deleted. Skill applied: `phased-work-handoff-designer`, for carrying
each class forward as a citable ID with its proven-invocation check, and for
recording explicitly what this page did **not** touch.
