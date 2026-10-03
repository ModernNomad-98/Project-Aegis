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

**Appended 2026-10-03 — this page now carries SEVEN classes, and `PROC-07` …
`PROC-13`.** The paragraph above says six; it is left exactly as written, because
this page's practice is to correct forward rather than rewrite a dated
measurement, and because the same rule applies to this page's own counts as to
any other evidence. **Class 7** was appended under the same five-part shape,
repeated **per defect** at one heading level deeper — `### 7.1` … `### 7.7`, each
with `#### Issue`, `#### Evidence`, `#### How it happened`,
``#### Standing rule — `PROC-NN` `` and `#### Detection check` — because one class
now records seven defects of one mechanism rather than one. Measured on the text
that carries it, the `## Class` headings number **7** and the distinct rule IDs
number **13**. Read `PROC-07` … `PROC-13` exactly as `PROC-01` … `PROC-06` are
read: run the detection check in the same turn, against the revision you are
acting on. **Six of the seven are dispatch-time rules whose violation leaves no
artifact**, so their detection checks are things a dispatcher runs about its own
behaviour — they are not gates that fail, and a rule believed to be a gate when
it is not is the third bullet under "Honest limits" below.

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
That trailing-newline state is what decides **which of the two deltas above
applies** — it is not the cause of the over-report. Measured at `6715cefc`,
where 32 of 1426 tracked blobs are unterminated:

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

**The second form: a split of the raw text, which over-reports unconditionally.**
The trap above describes only the form that splits an **array of lines**, whose
terminator was already discarded before the split ran. A **raw single-string
read** preserves the final terminator, and splitting that string on newline
returns **one more element than there are newline bytes — for a terminated blob
exactly as much as for an unterminated one.** The over-report is therefore
**unconditional** here, and it has a different cause: the **empty trailing
element** a final `0x0A` always produces, not a lost terminator. Measured in
PowerShell at `14f689e8`:

```text
$ (git show <rev>:<path> | Out-String) | Get-Member -MemberType Method
    # a raw read: ONE string, the final terminator preserved
$ ((git show 1b9e7049:docs/skills-catalog.md | Out-String).Split("`n")).Count
1493        # the true newline count is 1492 (PROC-04 method)      -> +1
$ ((git show 93c0834f:docs/skills-catalog.md | Out-String).Split("`n")).Count
1505        # the true newline count is 1504 (PROC-04 method)      -> +1
$ (Get-Content -Raw docs/skills-catalog.md).Split("`n").Count
1505        # same file on disk: 1504 `0x0A` bytes, last byte 0x0A -> +1
$ ('a' + "`n" + 'b' + "`n" + 'c' + "`n").Split("`n").Count
4           # a terminated fixture with 3 newlines                 -> +1
$ ('a' + "`n" + 'b' + "`n" + 'c').Split("`n").Count
3           # an UNTERMINATED fixture with 2 newlines              -> +1
```

Both forms over-report by 1, but for different reasons and under different
conditions, so neither may be used as a newline count: the **array** form's
+1 is conditional on the trailing-newline state and is 0 on a terminated blob,
while the **raw-text** form's +1 holds whether or not the blob is terminated.

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
trailing-newline change must be checked explicitly.** Both split forms above are
also forbidden for a line count — neither the array **element count** nor any
**split-on-newline** of such an array or of the raw text is a newline count, and
that covers the raw single-string form whose +1 is unconditional. Concretely:
state whether
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
`docs/evidence/session-continuation-2026-09-30-evening.md:176` and
`docs/roadmaps/aegis-documentation-readability-backlog.md:2772`
(`git grep -n 'Measure-Object -Line' origin/main -- '*.md'` at `origin/main` =
`1cb61f3a`, 2 hits) — and **every one of them is text *about* the trap, not a count
produced by it**. The list this paragraph first gave included this page as a third
hit; that was **wrong for `main`** and is corrected here: this page is not on `main`
at all (`git cat-file -e
origin/main:docs/evidence/documentation/process-issues-and-prevention-2026-10-02.md`
→ 128), so its own prohibition cannot be a hit there yet and becomes a third only if
this page merges. So a hit must be read, not failed on, and the list of hits is itself
a revision-bound figure. A mechanical version of this check needs an allowlist of
pages that define the rule. Any published count that fails to name its method fails
this check.

---

## Class 5 — acting on an unmerged artifact

### Issue

A tool that lives **inside an open, unmerged, unreviewed pull request** was used
to derive a finding — "159 pages have no review record" — and work was nearly
dispatched from that finding. It was caught before dispatch.

### Evidence

**PROVEN** for the artifact's status; **UNVERIFIED** for the figure.

**Dated correction, 2026-10-02, added by the fix pass that answered an independent
review of this page.** The figures in this block were read while PR #629 was open and
several have since moved — this document's own Class 3 defect appearing in its own
evidence. Re-measured as of `origin/main` = `1cb61f3a312d76afad6ec525155184abd120f24c`:
PR #629 is **MERGED** (`mergedAt` 2026-10-03T01:08:52Z), not `OPEN`; its head moved to
`797ca687`, not `7c52b6f6`; `gh pr view 629 --json files --jq '.files | length'`
returns **13**, not 12, the added path being
`tools/readability_acceptance/tests/test_verify_ground_truth.py`; and
`git cat-file -e origin/main:tools/readability_acceptance/check_index.py` now exits
**0**, so the last listing in the block is stale as well. The block is left verbatim
because this page's convention is to correct forward rather than rewrite a dated
measurement. **`PROC-01` applies to this correction too**: `797ca687` is the merged
PR's head and is **not** an ancestor of `origin/main` (`git merge-base --is-ancestor
797ca687 origin/main` → 1), because the merge squashed it — so the tool is on the
default branch as *content*, which is the test `PROC-01` requires, not as that commit.

```text
$ gh pr view 629 --repo ModernNomad-98/Project-Aegis --json state,mergedAt,headRefOid,title
state = OPEN   mergedAt = (empty)   head = 7c52b6f63dc14dd1cb794b486135c2d9eb988302
title = docs(tools): add a per-path readability acceptance index
$ gh pr view 629 --repo ModernNomad-98/Project-Aegis --json files
13 files at head 797ca687, all under:
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
tools/readability_acceptance
```

**Dated correction, same pass — what changed for `PROC-05` and what did not.** PR #629
merged at 2026-10-03T01:08:52Z, so the instrument is now on the default branch as
content and `PROC-05`'s "unmerged instrument" clause **no longer applies to it**. What
survives unchanged is the class's defect: at the time the "159 pages" figure was used,
the tool was unmerged and unreviewed, which is the act this class records. The `159`
figure is **still UNVERIFIED**, and the reason is now narrower and is stated rather than
inherited: this fix pass did not re-derive it. The honest obstacle, named so the next
reader is not misled: re-running it needs the merged tree in a working checkout, and
this lane's brief forbids creating worktrees or helpers, so no attempt was made.

The tool was absent from the default branch when the figure was produced, so its output
could not be re-derived there then, and this page's PR neither ran it nor authorized
running it. **The "159 no-record pages" figure is UNVERIFIED.** Anyone acting on that
figure must first re-derive it from `main`; the instrument now exists there, so that
re-derivation is now possible — which it was not when this class was written.

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
$ git show 145647cc:.claude/skills/rls-policy-auditor/SKILL.md | sed -n 218p
  per-command audit questions, the seven failure-mode catalog with detection
$ git show 5703e93f:.claude/skills/rls-policy-auditor/SKILL.md | sed -n 217p
  per-command audit questions, the seven failure-mode catalog with detection
$ git show d9f57283:.claude/skills/rls-policy-auditor/SKILL.md | sed -n 218p
  per-command audit questions, the seven failure-mode catalog with detection
```

**The line is identical; the file was not — and at the current `origin/main` the
blobs are identical too.** Two corrections to what this paragraph first said, both
measured 2026-10-02 and both **PROVEN**.

*The citation was off by one for `145647cc`.* The quoted text sits at line **218**
in that revision's blob, not line 217, which is the `references/…` link line. The
block above now gives each revision the number it actually needs, because the two
blobs do not share a line numbering: the one carrying the reconciliation citation
has one more line above this point (raw `0x0A` byte counts, the method `PROC-04`
requires: 223 against 222). The original block showed `sed -n 217p` for both
revisions with one identical output, which the first of those two commands cannot
produce. Those runs used Git's bundled `C:\Program Files\Git\usr\bin\sed.exe`,
which is not on `PATH` in the measuring environment.

*The blob-difference claim is now false.* This paragraph read:

> The blobs differ — `cf8d207f` at `145647cc` against `3d25584f` on `origin/main` —
> because the branch also carries `a69d4d1f`'s reconciliation citation. A verifier
> comparing whole-file hashes would report a false mismatch, and the count that had
> to match does match.

`3d25584f` is the blob at `5703e93f` — the revision this class records as
`origin/main` four paragraphs above — not at the `origin/main` that exists now.
Measured after `git fetch origin` in `C:\src\Project Aegis\wt-register`:

```text
$ git rev-parse origin/main
d9f57283145ce2608ff76920dddd3db5be48b9a9
$ git rev-parse 145647cc:.claude/skills/rls-policy-auditor/SKILL.md
cf8d207f190bf4024b4ba09b8afd186d73870d6a
$ git rev-parse 5703e93f:.claude/skills/rls-policy-auditor/SKILL.md
3d25584f5f0d21cfeb36f191a93ab215af77f23e
$ git rev-parse f6bf9d9a:.claude/skills/rls-policy-auditor/SKILL.md
cf8d207f190bf4024b4ba09b8afd186d73870d6a
$ git rev-parse d9f57283:.claude/skills/rls-policy-auditor/SKILL.md
cf8d207f190bf4024b4ba09b8afd186d73870d6a
```

`145647cc` and the current `origin/main` are therefore the **same blob** for that
path, and the mismatch closed at `f6bf9d9a` (PR #632), which carries `cf8d207f` —
the file the branch already had. The cause the original sentence gave is confirmed
rather than withdrawn: `git diff 3d25584f cf8d207f` is **3 insertions and 2
deletions**, all inside the reconciliation §3 citation. **PROVEN.**

**What survives, and what does not.** The conclusion survives: the file at
`145647cc` carries the `seven` text and so does the current `origin/main`, so the
owed correction stays discharged and the `seven` finding is untouched. What does
not survive is the illustration — a verifier comparing whole-file hashes now gets a
*true* match, not the false mismatch this paragraph warned against. The lesson
drawn from it stands unchanged: this is `PROC-01`'s lesson in miniature, run the
test that answers the question asked and do not let a broader test answer a
narrower one. Its durable part is the revision binding — a figure read from a
moving ref must carry the revision it was read at, or the next reader inherits a
falsehood instead of a measurement.

**This is the register's own subject matter, and this instance went undisclosed.**
The false half was a value read from the moving ref `origin/main` and written down
without the revision it was read at, so main moving made it false. That is Class
3's defect — a measurement carried forward without its instant — and Class 1's
hazard seen from the other side: a claim true of the ref as it then stood and false
of the ref a reader now looks at. This class already records that drift twice, for
the "never pushed" claim and for its own provenance; unlike those, this one was not
noticed. Both provenance notes re-checked "Classes 1–5" at the new tip and left this
class's own figures unexamined, and the sentence survived both correction passes.
One `git rev-parse` falsifies it. This page's own branch still carries `3d25584f`
for that path and does not modify it (`git diff --name-only 6715cefc..HEAD` lists
only this document), so the stale copy is inert and merging cannot revert `main`'s
file.

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

**A fifth drift, in the same provenance, re-measured by the fix pass that answered an
independent review of this page on 2026-10-02, and this one is a different kind.** The
note immediately above is a dated measurement and has drifted in turn, exactly as it
predicted. Re-measured at `origin/main` = `1cb61f3a312d76afad6ec525155184abd120f24c`,
`git rev-list --count 6715cefc..origin/main` → **10**, not the **4** recorded there;
that 4 was true at `d9f57283`, the tip the note names, so the figure is corrected to
name its revision rather than replaced with a number that will be stale by the next
reader. Of the four checks the note lists, **three still hold** and **one does not**:
`git grep -n "Each base SHA is the page's last recorded acceptance" origin/main --
docs/roadmaps/aegis-documentation-readability-backlog.md` still hits line 2790;
`git merge-base --is-ancestor 65bacc7d6b85 origin/main` still exits 1;
`git cat-file -e origin/main:tools/readability_acceptance/check_index.py` now exits
**0**, because PR #629 merged at 2026-10-03T01:08:52Z — so **"PR #629 is still `OPEN`"
is false at `1cb61f3a`**. That is the fifth drift this class has recorded in its own
provenance and the first one that changed a *conclusion* rather than only a number,
which is why Class 5 carries its own dated correction above. This note is a dated
measurement too, and will drift in turn.

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

## Class 7 — reading an observation as the fact: silent exits, stranded work, failed commands and single samples

### Issue

`PROC-06` already records **one** form of this mechanism: "absence of commits is
NOT evidence of an inactive lane". This class records the **seven further forms
observed in the same session**, each with its own command and its own rule. The
shared mechanism is one sentence: **an observation that is true of the repository
is read as a fact about the lane, the command, the sample or the estimate it does
not describe.** The observation is accurate; the inference is not.

| # | Defect | Rule | Evidenced here |
| --- | --- | --- | --- |
| 7.1 | A dispatch ends with no artifact at all, and the lane looks healthy | `PROC-07` | artifact timelines PROVEN; dispatch counts UNVERIFIED |
| 7.2 | Work is committed and pushed with no pull request (`pushed ≠ proposed`) | `PROC-08` | branch, commit and PR PROVEN; push instant NOT DERIVABLE |
| 7.3 | A command's failure, or its absence, or its coverage, is read as a fact about its subject | `PROC-09` | all four mechanisms PROVEN; one historical instance UNVERIFIED |
| 7.4 | Fire-and-forget delegation forces polling, and polling duplicates | `PROC-10` | a byte-identical duplicate record PROVEN; the second merge dispatch UNVERIFIED |
| 7.5 | One or two samples are read as a distribution | `PROC-11` | the distribution PROVEN; the run it was applied to UNVERIFIED |
| 7.6 | The coordinator's own estimates are the least reliable input | `PROC-12` | five falsified figures PROVEN, one that verified PROVEN |
| 7.7 | Two review dispatches overlap at one head | `PROC-13` | both duplicate pairs PROVEN |

Six of the seven are defects of the coordinator's dispatch-and-verification loop.
The seventh (`7.6`) is the coordinator's **own numbers as an input to that loop**,
and it is recorded at the same weight because it is the input the other six are
built on.

Each defect below carries the five-part shape used by Classes 1–6 — **Issue /
Evidence / How it happened / Standing rule / Detection check** — repeated at one
heading level deeper, because one class now records seven defects of one
mechanism rather than one. Where a defect's subject is session state that no
repository artifact records, the section says so and labels the claim
`UNVERIFIED` rather than presenting it as evidence; that labelling is not a
formality, it is the subject of `7.1` and `7.3` applied to this page itself.

---

### 7.1 — a dispatch that ends with no artifact at all

#### Issue

A dispatched subagent can end its turn having produced **nothing** — no pull
request comment, no commit, no message — while its lane looks healthy from the
outside. Nothing in this repository distinguishes such a dispatch from one that
was never made, because the environment is exactly what the silent dispatch did
not change.

#### Evidence

**PROVEN** for the artifact timelines. **UNVERIFIED** for every dispatch count,
with the reason stated.

Read from the GitHub API on 2026-10-02/03. PR #643's full comment history,
enumerated rather than summarised:

```text
$ gh api repos/ModernNomad-98/Project-Aegis/issues/643/comments --paginate
2026-10-03T01:12:51Z  chatgpt-codex-connector[bot]  id=5963982501
2026-10-03T01:16:24Z  ModernNomad-98                 id=5964009983
2026-10-03T01:16:32Z  chatgpt-codex-connector[bot]  id=5964010990
2026-10-03T01:18:33Z  ModernNomad-98                 id=5964026193   first review record
2026-10-03T01:21:08Z  ModernNomad-98                 id=5964045603   link fix
2026-10-03T01:29:39Z  ModernNomad-98                 id=5964118480   CODE REVIEW
2026-10-03T01:29:47Z  ModernNomad-98                 id=5964119436   CODE REVIEW
2026-10-03T01:29:56Z  chatgpt-codex-connector[bot]  id=5964120478
2026-10-03T01:30:51Z  ModernNomad-98                 id=5964127358
2026-10-03T01:31:02Z  chatgpt-codex-connector[bot]  id=5964128766
mergedAt = 2026-10-03T01:31:17Z
```

The longest artifact-free interval on that pull request is **8 min 31 s**,
between `5964045603` (01:21:08Z) and `5964118480` (01:29:39Z). The same listing
for PR #645 gives three comments — `5964156617` (01:34:49Z), `5964180232`
(01:37:59Z), `5964191494` (01:39:33Z) — whose longest artifact-free interval is
**3 min 10 s**, inside a pull request whose whole life was **5 min 15 s**
(`createdAt` 01:34:45Z, `mergedAt` 01:40:00Z).

A second, independent record gap is **on the default branch**.
`.coord/coordinator-cadence.jsonl` is tracked, and its own line 5 states the
rule: *"Appending each check to THIS tracked file is a required step of the
cadence … A check that was not appended here cannot be told apart from one that
did not run."* Its last `checked_at` is `2026-10-02T18:18:37-07:00` =
`2026-10-03T01:18:37Z` (18 distinct `checked_at` values over 23 lines), and
**four merges landed after it**:

```text
$ gh pr view <n> --json number,mergedAt,mergeCommit
#633  mergedAt=2026-10-03T01:24:02Z  e88a0a0d
#643  mergedAt=2026-10-03T01:31:17Z  d10f6319
#644  mergedAt=2026-10-03T01:35:59Z  3adebe6d
#645  mergedAt=2026-10-03T01:40:00Z  3c58e966
```

**What could not be evidenced, and why that absence is the finding.** The
briefed account is that at least three review dispatches returned no record at
all, that a pull-request comment count stayed flat over several minutes, that one
merge dispatch returned nothing while the pull request stayed open, and that one
review task replied *"NO GAP, nothing written"* correctly. **None of that is
verifiable from this repository and none of it is asserted here.** A dispatch is
session state; a dispatch that produces no artifact leaves no ref, no file, no
comment and no log line. **`UNVERIFIED`.**

Also `UNVERIFIED`: that PR #645's merge required a **second** merge dispatch.
What the repository records is one merge per pull request, by a human account:

```text
$ gh api repos/ModernNomad-98/Project-Aegis/issues/643/timeline --paginate
2026-10-03T01:31:17Z | merged | ModernNomad-98
$ gh pr view 643 --json mergedBy
mergedBy = { login: "ModernNomad-98", is_bot: false, name: "Peter Nguyen" }
$ gh api repos/ModernNomad-98/Project-Aegis/pulls/643/reviews | ConvertFrom-Json | .Count
0
```

And `UNVERIFIED`: whether an idle check was **due** between 01:18:37Z and
01:40:00Z. The four post-log merges show the window contained landings; they do
not show the cadence required an entry in it. The gap is therefore recorded as a
**record gap of unknown obligation**, not as a missed check.

#### How it happened

The dispatch channel is one-way **for failures**. A dispatched agent that
succeeds writes to a shared surface — a comment, a commit, a ref. A dispatched
agent that ends early writes nothing, and there is no separate "I ended" channel
to write to. The coordinator therefore has exactly one observable, the shared
surface, and reads "no new artifact" as "no result **yet**", which is
indistinguishable from "no result **ever**". This is `PROC-06`'s mechanism seen
from the other side: there the coordinator read an absent artifact as *dead*,
here as *still working*. Both are inferences from an observation that does not
carry the information.

The second half is the brief's wording. A dispatch that says "review this and
report" makes the report **optional in practice**, because an agent that finds
nothing to say has no artifact it must produce. "Nothing to report" and "did not
run" then look identical on the pull request — which is precisely the state
`7.3` forbids reading as a result.

#### Standing rule — `PROC-07`

**Every dispatch must state its deliverable as mandatory, and the deliverable
must be an artifact on a shared surface.** A dispatch whose deliverable is a
judgement must instruct the agent to **write and post the judgement even when the
judgement is "no gap"**: if the agent is unsure, it writes `unsure` and posts
anyway. **A written gap is the deliverable; silence is not.** A dispatch that
cannot name the artifact it expects — which comment, which commit — does not
satisfy this rule, and where the artifact cannot be named, prefer the
durable-teammate form of `PROC-10`.

#### Detection check

Do not verify a dispatch by elapsed time. **Enumerate the artifacts it was
supposed to produce, by identity, and check for those**:

```text
$ gh api repos/ModernNomad-98/Project-Aegis/issues/<pr>/comments --paginate
$ gh pr view <pr> --repo ModernNomad-98/Project-Aegis --json headRefOid,mergedAt,mergedBy
$ git log --format='%h %cI %s' <base>..origin/main
```

Then answer in writing: **which comment id, or which commit SHA, was expected,
and is it present?** A dispatch whose expected artifact is absent is
**unverified**, not **in progress**. And because an absent artifact cannot be
distinguished from an unrun dispatch, the honest entry in a record is
`UNVERIFIED` — never "the agent reported nothing", which asserts a report that by
construction does not exist.

---

### 7.2 — work that is committed and pushed with no pull request (`pushed ≠ proposed`)

#### Issue

Work can be completed, committed **and pushed** while no pull request exists. It
is then invisible to every queue-based coordination rule this repository has: the
review queue, the merge queue and `gh pr list` all read pull requests, and a
pushed branch is not one.

#### Evidence

**PROVEN** for the branch, its commit and its pull request. **NOT DERIVABLE** for
the push instant.

```text
$ git ls-remote --heads origin chore/cadence-log-append-3
0f62022defedc32b27db3db1576f004a58eb0fea	refs/heads/chore/cadence-log-append-3
$ git log -1 --format='%H%n%cI%n%s' 0f62022d
0f62022defedc32b27db3db1576f004a58eb0fea
2026-10-02T18:22:40-07:00
chore(coord): append six evidenced coordinator idle-check entries
$ gh pr list --repo ModernNomad-98/Project-Aegis \
    --head chore/cadence-log-append-3 --state all --json number,state,createdAt
[{"number":644,"state":"MERGED","createdAt":"2026-10-03T01:26:49Z"}]
```

The branch's tip commit is stamped `2026-10-02T18:22:40-07:00` (= `01:22:40Z`)
and its **only** pull request, **#644**, was created at `2026-10-03T01:26:49Z` —
**4 min 9 s later**. #644 merged at 01:35:59Z as `3adebe6d`.

**The push instant is NOT DERIVABLE, and is not asserted.** GitHub exposes no
ref-push timestamp for `refs/heads/chore/cadence-log-append-3`: the repository
events feed returns 52 `PushEvent`s for this repository and that ref is **not**
among them — the refs seen include `refs/heads/chore/cadence-log-append-2` but
not `…-append-3`:

```text
$ gh api repos/ModernNomad-98/Project-Aegis/events --paginate
push_events_returned = 52
refs seen include refs/heads/chore/cadence-log-append-2, refs/heads/main
refs/heads/chore/cadence-log-append-3  -> ABSENT
```

A commit's own instant is not its push's instant, so the interval during which
the branch was on the remote with no proposal **cannot be measured** from this
repository.

**A bounded sweep finds no stranded branch today — a negative result, not a
clearance.** All **26** remote branches whose tip commit is dated 2026-10-02 or
2026-10-03 have exactly one `MERGED` pull request each:

```text
$ git for-each-ref --sort=-committerdate refs/remotes/origin \
    --format='%(committerdate:iso8601-strict)|%(objectname)|%(refname:short)'   # filtered 2026-10-0[23]
$ gh pr list --repo ModernNomad-98/Project-Aegis --head <branch> --state all     # per branch
26 branches | 26 with a MERGED PR | 0 with no PR        # origin and main excluded; they are not lanes
```

A stranded branch is therefore a **transient** state: it is observable only while
it lasts, and the mapping above says nothing about whether any branch was
stranded earlier and proposed later. The sweep's value is the check, not the
result.

**`UNVERIFIED`:** that a second instance occurred earlier in the same session
with the same shape, and that on #644 one agent opened the pull request while a
second was dispatched to do so and correctly created nothing. Both are session
state. The repository records one pull request per branch and no duplicate.

#### How it happened

The lane's unit of work ended at `git push`, and push is the last step any *git*
command can confirm. Opening a pull request is a separate act on a different
system with a different failure mode, and nothing in the lane's recipe made it
part of the definition of done. So "done" was reached with the work complete and
unproposed, and the coordinator's queue — which reads proposals — saw nothing at
all. Note what this does **not** require: no mistake by the lane. `PROC-06`'s
second-writer hazard needs a race; this one needs only that the lane stop one
step early.

#### Standing rule — `PROC-08`

**A lane is not done until its pull request exists. A push is not a proposal, and
a commit is not a queue entry.** The lane's definition of done includes the pull
request, and the dispatcher verifies the **proposal** rather than the branch.
**Before dispatching any task whose purpose is to open a pull request, run
`gh pr list --head <branch> --state all` first** — a task to create an object
that already exists is a task to create a second one, and two agents dispatched
at one object race exactly as `PROC-02` and `PROC-06` describe.

#### Detection check

```text
$ git ls-remote --heads origin <branch>
$ gh pr list --repo ModernNomad-98/Project-Aegis --head <branch> --state all \
    --json number,state,createdAt,mergedAt
```

A ref on the remote with an empty `gh pr list` result is stranded work. Run the
second command **in the dispatcher's turn**, not in the agent's, because the
agent's answer is the artifact whose existence is in question. To sweep without
knowing the branch:

```text
$ git for-each-ref --sort=-committerdate refs/remotes/origin \
    --format='%(committerdate:iso8601-strict)|%(refname:short)'
```

This is the one check in this class that is a **complete** detector over the refs
it reads: unlike `PROC-07`, an empty result here is a real finding, because a
stranded branch leaves a readable artifact — the ref itself.

---

### 7.3 — a command's failure read as a fact about its subject

#### Issue

Three separate failures in this session share one mechanism, and **a fourth was
found in this run** while verifying this class's own pull request: **a command
failed, and its failure — or the absence of the command — was read as a fact
about the thing the command was supposed to measure.** A failed command carries
no information about its subject; it carries information about the command.

#### Evidence

**PROVEN** for all four mechanisms, each reproduced in this run. **UNVERIFIED**
for the first instance's historical record, with the search stated.

**(a) A failed `git show` emits a line, and a line can be counted as content.
Reproduced:**

```text
$ git show '6715cefc:scripts/ci/check-markdown-links.py' 2>&1 | <count>
1
$ git show '6715cefc:scripts/ci/check-markdown-links.py' 2>&1
fatal: path 'scripts/ci/check-markdown-links.py' does not exist in '6715cefc'
$ git cat-file -e '6715cefc:scripts/ci/check-markdown-links.py' ; echo $?
128
```

The pipeline's output is **non-empty — one line — while the path does not
exist.** Any measurement that asks "did this produce content?" or counts output
lines answers *yes* and *1* for an absent path. The exit code is the only part of
that run that describes the subject, and it says `128`.

The pair of file states the briefed instance turns on is real, and both sides
were measured here:

```text
$ git cat-file -e 724644aa:docs/evidence/approvals/APPROVAL_REGISTER.md ; echo $?
128                                   # absent at the reviewed head
$ git cat-file -e 5d99a373:docs/approvals/APPROVAL_REGISTER.md ; echo $?
0                                     # present after the fix
$ git cat-file -s 5d99a373:docs/approvals/APPROVAL_REGISTER.md
193671                                # size, from the object store, not from printed output
```

**What could not be evidenced.** The briefed instance is that a coordinator
measurement counted a failed `git show`'s error line as file content and reported
a file as **present** when `git cat-file -e` returned **128**. **No repository
artifact records that measurement, and the search is stated:** 138 issue comments
across PRs #613–#646 were harvested, and searches for `does not exist in`,
`fatal: path`, `can't open file`, `cat-file -e` and `rev-parse --verify` return
only records that use the **correct** method — PR #643's two review records
(`5964118480`, `5964119436`) each cite `git cat-file -e` → exit 0 with
`git cat-file -s` size, and the control at the reviewed head → exit 128. The
untracked session scratch under `artifacts/coord/` was searched the same way and
holds no such record. **`UNVERIFIED` for the instance; PROVEN for the mechanism.**

What **is** recorded, and is the nearest evidenced instance of the same family,
runs the other way: **an assertion of a verification result that no run
supported.** PR #643's body asserts *"Every link and anchor added by this diff was
resolved against the actual files … all resolve."* The same pull request carries
the correction: *"The **path** half was false … reproduced here as
`python -B scripts/ci/check-markdown-links.py docs/` → **broken 2, exit 1** at
prior head `724644aa`."* The assertion was published; a measurement falsified it.

**(b) A transient `rev-parse --verify` failure read as a fact about the object.**
The briefed instance is that an agent inferred from a transient failure that
`1cb61f3a` "is not main". The subject fact is PROVEN the other way:

```text
$ git rev-parse --verify 1cb61f3a
1cb61f3a312d76afad6ec525155184abd120f24c
$ git cat-file -t 1cb61f3a
commit
$ git merge-base --is-ancestor 1cb61f3a origin/main ; echo $?
0
```

`1cb61f3a` is the squash commit of PR #629, is a `commit`, and **is** an ancestor
of `origin/main`. Five consecutive `rev-parse --verify 1cb61f3a` runs in this turn
each exited **0**, so the transient failure **did not reproduce** and is
`UNVERIFIED`; what is PROVEN is that the claim it produced is false of the object.

**(c) A missing tool is not a result. Reproduced live in this run.** The mandated
link checker was absent from the `coord-main` working tree, and the mandated
command failed with Python's own missing-file error:

```text
$ Test-Path 'C:\src\Project Aegis\coord-main\scripts\ci\check-markdown-links.py'
False
$ git cat-file -e 797ca687:scripts/ci/check-markdown-links.py ; echo $?     # coord-main's HEAD
128
$ python -B scripts/ci/check-markdown-links.py docs/
C:\Python314\python.exe: can't open file
  'C:\src\Project Aegis\coord-main\scripts\ci\check-markdown-links.py': [Errno 2] No such file or directory
$ echo $?
2
```

Exit **2** with "can't open file". The checker exists on the default branch —
`git cat-file -e 3c58e966:scripts/ci/check-markdown-links.py` → **0** — and did
not exist at `6715cefc`, `b0d3ab71` or `d9f57283` (**128** at each); it arrived
with PR #628's `b97ff272` (**0**). The working tree is stale relative to
`origin/main`, so the tool is missing **there** while present on the default
branch. **Reading exit 2 as "0 broken" is the defect**; the correct reading is
"the check did not run", and the correct remedy is to run it from a revision that
has it — which this class's own pull request did, in a worktree at `origin/main`.

**(d) A tool that reports `0` is reporting `0` about the subset it can see.
Found in this run, while verifying this class's own pull request.** The mandated
checker was run at the base and at the change and returned the **same** counts
both times:

```text
$ python -B scripts/ci/check-markdown-links.py docs/      # at the base 3c58e966
files: 212   links checked: 2388   anchors checked: 704   broken: 0   dead: 0   external-skipped: 1691
$ git diff -U0 -- docs/evidence/.../process-issues-and-prevention-2026-10-02.md | grep -c '^+.*https\?://'
6                                                          # six external links ADDED
$ python -B scripts/ci/check-markdown-links.py docs/      # at the change
files: 212   links checked: 2388   anchors checked: 704   broken: 0   dead: 0   external-skipped: 1691
```

Six added links, **not one** of them counted. The cause is in the checker, not in
the change:

```text
$ grep -n '^LINK' scripts/ci/check-markdown-links.py
32:LINK = re.compile(r"\[([^\]\n]*)\]\(\s*(<[^<>\n]*>|[^()\n]*?)\s*\)")
$ grep -n 'for line_number, line in' scripts/ci/check-markdown-links.py
145:        for line_number, line in enumerate(doc.body.splitlines(), start=1):
146:            if "](" not in line: continue
```

The loop is **per line** and the pattern's character classes are `[^\]\n]` and
`[^()\n]` — newlines are explicitly excluded. A Markdown link whose `[text](`
or `(target)` straddles a line break therefore **cannot match**, so it is never
counted, resolved, or reported as broken. That is what the first run of this
class's own append did: the six links were wrapped after `[PR #643 comment`, and
the checker's identical counts were the only symptom.

**Un-wrapping them moved the counts — and the honest part is *which* count
moved.** After the fix:

```text
$ python -B scripts/ci/check-markdown-links.py docs/      # at the change, links un-wrapped
files: 212   links checked: 2388   anchors checked: 704   broken: 0   dead: 0   external-skipped: 1697
```

`external-skipped: 1691 → 1697` — **exactly six, the six added links, which
confirms the cause.** `links checked` stayed at **2388**, and that is correct
behaviour, not a second defect: `check-markdown-links.py:152-155` increments the
`external` counter and `continue`s, so `counts['checked'] += 1` at line 171 is
reached only by an **internal** link the tool resolves. **This class's own first
prediction was that both counters would move by six, and the measurement falsified
it** — recorded here rather than quietly corrected, because it is `7.6`'s defect
occurring inside the section that documents `7.6`. The lesson is narrower and
sharper than "the count must move": **identify which counter covers the item you
added before concluding anything from it.**

A second, smaller instance of the same mis-count sits in the command above.
`grep -c '^+.*https\?://'` returns **1** for those six links once they are on one
line — that command counts **lines containing a URL**, not URLs. It said 6 only
while the links were wrapped one per line. A count is only ever a count *of the
thing the command counts*.

**This is `7.3`'s mechanism in its most comfortable form.** The command
**succeeded**, exited `0`, and printed `broken: 0` — and `0` was true *of the
links the tool could see*. Reading it as "this document's links are fine"
substitutes the tool's coverage for the claim. The same reading is what made
Class 5's figure provisional and what `PROC-05` is about. The prevention rule is
`PROC-09`'s third clause extended: **when a check reports a clean result, verify
that the check can see the thing you added** — a count that does not move when
the input grows is evidence of a coverage gap, and the honest fix is to make the
artifact visible to the tool, not to accept the zero.

#### How it happened

A shell pipeline flattens two different things into one channel: what the command
**said**, and whether it **succeeded**. Where the two disagree — a failure that
prints, a success that prints nothing, a command that never started — the printed
text is the part a reader sees first and the exit status is the part easiest to
drop. `PROC-04`'s trap is the same shape one layer up: a command that **succeeds**
and prints a number that does not mean what it appears to mean. Between them,
`PROC-04` and this section say one thing: **the printed text is not the
measurement, in either direction.**

#### Standing rule — `PROC-09`

**A command's failure is a fact about the command, never about its subject.**
Three rules follow. **Existence is read from an exit code** — `git cat-file -e
<rev>:<path>`, exit `0` present and `128` absent — **and size from
`git cat-file -s`**; never from a command's printed output, and never from
whether output was produced at all. **On any failed command, re-run it before
concluding anything about the subject**: a single failure is `UNVERIFIED`, not
evidence, and the correct record names the failure observed and states that it
did not reproduce. And **distinguish "the tool is missing" from "the tool
reported a result"** — a checker that cannot start has cleared nothing, and its
absence is reported as **unrun coverage**, exactly as an unrun `pwsh` step is.
**And a check that reports a clean result must be shown to cover the thing you
added**: a count that does not move when the input grows is a coverage gap, not a
pass, and the remedy is to make the artifact visible to the tool rather than to
accept the zero.

#### Detection check

```text
$ git cat-file -e <rev>:<path> ; echo $?          # 0 present | 128 absent
$ git cat-file -s <rev>:<path>                    # size in bytes, from the object store
$ <command> ; echo $?                             # capture the status, not the text
```

Before publishing any sentence of the form "the file exists", "the path is
present", "the tool found 0 problems" or "the command reported", answer: **which
exit code establishes this, and was it this run's?** A claim resting on printed
output, or on a command that exited non-zero, fails this check.

For the coverage clause, the check is arithmetic on the tool's own summary:

```text
$ <the tool> <scope>            # record links checked / files / items counted
$ <add one instance of the thing the tool checks>
$ <the tool> <scope>            # the count MUST move; if it does not, the tool cannot see it
```

A count that is unchanged after the input grew means the added instance is outside
the tool's coverage. Record it as **uncovered**, never as passing — and identify
**which counter** covers the item you added first, because counters within one
tool cover different classes: in `check-markdown-links.py`, `external-skipped`
counts external links and `links checked` counts only internal ones the tool
resolved, so an external link can be counted by one and never by the other.

---

### 7.4 — fire-and-forget delegation, coordinator polling, and the duplication it produces

#### Issue

A background dispatch has **no addressable target, no status and no completion
signal**. The coordinator cannot ask it anything, cannot read its state, and
cannot be told it finished; it can only re-read the environment and infer. The
cost of that inference is duplication, and duplication on a state-changing action
is how two agents come to hold one object.

#### Evidence

**PROVEN** for the merge that two agents were in a position to perform, and for
the duplication this mechanism has already produced. **UNVERIFIED** for the
two-dispatch claim itself.

PR #643 is merged **once**, by a human account, at a single instant:

```text
$ gh api repos/ModernNomad-98/Project-Aegis/issues/643/timeline --paginate
2026-10-03T01:31:17Z | merged | ModernNomad-98
2026-10-03T01:31:17Z | closed | ModernNomad-98
$ gh pr view 643 --json mergedAt,mergedBy
mergedAt = 2026-10-03T01:31:17Z
mergedBy = ModernNomad-98   (is_bot: false, name "Peter Nguyen")
$ gh api repos/ModernNomad-98/Project-Aegis/pulls/643/reviews | ConvertFrom-Json | .Count
0
```

One `merged` event. **The repository cannot record a merge agent that found the
pull request already merged and correctly reported instead of forcing it**,
because that agent's correct action leaves exactly this state. The briefed
account — two merge agents on #643, the second observing `mergedAt` eleven
seconds before its first command — is therefore **`UNVERIFIED`**: the merge
instant is PROVEN, the second dispatch is not.

**The duplication this mechanism produces is recorded, and it is on the default
branch.** `.coord/coordinator-cadence.jsonl` line 8 (entry
`2026-10-02T17:01:00-07:00`) is a tracked, merged record by the coordinator of
its own process flaw: it dispatched a record-posting agent **without knowing
another agent had already posted the record**, so *"the security review stage is
now recorded twice on PR #623 from the same identity"*. The duplicate is
measurable, and the two comments are **byte-identical**:

```text
$ gh api repos/ModernNomad-98/Project-Aegis/issues/comments/5963358410   # 2026-10-03T00:00:08Z
$ gh api repos/ModernNomad-98/Project-Aegis/issues/comments/5963363229   # 2026-10-03T00:00:39Z
same_body = True
SHA-256 of body = 7080D2F7E028EA1C8B4170021B882885AC69EAB0F7BFBF8FDD2037B439D33332   # both
```

A byte-identical governance record posted twice, 31 seconds apart, from one
identity, is what a fire-and-forget dispatch duplicated by a second
fire-and-forget dispatch looks like in the artifacts. When the duplicated action
is a **record**, the cost is a duplicate. When it is a **merge**, the second agent
holds a state-changing verb on an object another agent may be changing — and the
only reason #643 cost nothing is that the second agent checked first.

#### How it happened

`PROC-06` describes the dispatch-time half of this: the coordinator re-dispatched
because an absent artifact looked like a dead lane. This section records the
**channel** half: the dispatch form itself carries no identity, so the
coordinator has no way to ask "are you still working?" and no way to be told
"done". Its only instrument is the environment, polled repeatedly, and a poll of
the environment cannot distinguish "not done yet" from "done, and the artifact is
elsewhere" from "never started". The duplication is not carelessness; it is the
only move available to an agent holding a one-way channel and a state-changing
task.

#### Standing rule — `PROC-10`

**For anything long-running or state-changing, prefer a durable teammate with a
task-board entry over a fire-and-forget dispatch.** A task-board entry gives the
work an address, a status and a completion signal — exactly what the dispatch
form lacks. **When a fire-and-forget dispatch must be used, record the expected
artifact and its identity — which comment id, which commit SHA — and check for
that artifact rather than for elapsed time or for a re-read environment.**
`PROC-07` makes the artifact **mandatory**; this rule makes it **addressable**.
Where two dispatches could reach one state-changing object, the second must
re-read the object's terminal state first and **report rather than act**: on
#643 the correct outcome was a report, and the state the repository shows is the
right one.

#### Detection check

Before dispatching, write down the artifact that will prove completion, in a form
that can be looked up:

```text
expected_artifact = comment id | commit SHA | PR number + state
```

Then, when checking, look up **that artifact** and no weaker proxy:

```text
$ gh api repos/ModernNomad-98/Project-Aegis/issues/comments/<id>
$ git cat-file -e <sha>^{commit} ; echo $?
$ gh pr view <pr> --json state,mergedAt,mergedBy
```

A check that reads elapsed time, a worktree listing, or an "is anything still
running" question is not this check. And for a **state-changing** dispatch, the
first command in the agent's turn must re-read the object's own state:

```text
$ gh pr view <pr> --repo ModernNomad-98/Project-Aegis --json state,mergedAt,mergedBy
```

If the object is already in its terminal state, the artifact is a **report**, not
an action.

---

### 7.5 — one sample read as a distribution

#### Issue

A fault was inferred from one or two observations without first establishing what
normal looks like. Nothing was wrong: the measurement of "how long does this
normally take" had never been taken.

#### Evidence

**PROVEN** for the distribution and its method. **UNVERIFIED** for which run the
conclusion was drawn about.

Measured in this run, **job-level** (`started_at` → `completed_at`) for the
`tools-tests-windows` job of each run:

```text
$ gh api repos/ModernNomad-98/Project-Aegis/actions/runs/<id>/jobs
run 37084966265  1cb61f3a   149 s
run 37085362907  f092b1e6   151 s
run 37085476795  f1d4e326   167 s
run 37086708014  3adebe6d   179 s
run 37085706454  5d99a373   180 s
run 37085288324  6c4471b2   216 s
run 37086629637  3e509264   217 s
run 37086126837  0f62022d   220 s
run 37085597971  583b330a   224 s
run 37086413143  d10f6319   227 s
run 37085944404  e88a0a0d   227 s
run 37084348600  38cd81ba   239 s
run 37083548224  b97ff272   240 s
n = 13, range 149-240 s                     # job-level method, stated
```

The briefed baseline for the check that was called a stall — `149 s, 151 s,
167 s, 216 s, 224 s, 227 s, 227 s` — **reproduces exactly** as seven values inside
that 13-run sample, by the same method, and each was traced to its own run id and
head SHA above. A run at the **top** of the range is not an anomaly. Recorded
here for `7.6`'s sake as well: this is a coordinator figure that **verified**.

**What could not be evidenced:** which run was called a stall, and the two polls
that called it so. A poll is session state. **`UNVERIFIED`.** What is PROVEN is
the distribution and the method.

**A method caution, in `PROC-04`'s spirit.** Run-level duration
(`run.created_at` → `run.updated_at`) and job-level duration are **different
measurements** and give different numbers for the same run:

```text
run 37084966265   run-level 232 s      tools-tests-windows job-level 149 s
$ gh run list --json databaseId,createdAt,updatedAt         # the run-level route
```

The briefed figures are reproducible **only** by the job-level method. A baseline
that does not name its method is `PROC-04`'s defect in a new unit.

#### How it happened

A long-running check is indistinguishable from a stall at any single instant, and
a poll produces instants. The first poll says "not finished"; the second says "not
finished"; two identical observations then read as a trend. The coordinator had no
baseline because it had never needed one — it had never previously had to decide
whether a duration was anomalous, so it had never measured the normal duration,
and the anomaly decision was made on the only two samples that existed. This is
`PROC-07`'s shape again with time in place of artifacts: the observation ("not
finished") is true and does not describe the subject ("stalled").

#### Standing rule — `PROC-11`

**Before calling a duration, a count or a rate anomalous, measure the baseline
from several prior instances and state the range, the count and the method.** One
observation is not a distribution; two are not a baseline. Where the baseline
cannot be measured from several instances, the correct output is **`unsure`**,
not "stalled" — and where the subject is a running check, the cost of waiting is
bounded by the measured normal duration, so state that bound instead of a verdict.

#### Detection check

```text
$ gh api repos/ModernNomad-98/Project-Aegis/actions/runs/<id>/jobs
    # per job: "name", started_at, completed_at      -> JOB-LEVEL duration
$ gh run list --json databaseId,createdAt,updatedAt  # RUN-LEVEL; different numbers
```

Compute the same job's duration across **at least five** prior runs and report the
range, the count and the method. Then:

```text
observed = <this run's elapsed>
baseline = <min> .. <max> over <n> prior runs      # n must be stated
```

An observation **inside** the baseline range is not an anomaly. Only an
observation outside it is a candidate, and even then the claim is "outside the
measured range of the last *n* runs", never "stalled".

---

### 7.6 — the coordinator's own estimates are the least reliable input

#### Issue

Across the session the figures the coordinator supplied were repeatedly
contradicted by measurement. The pattern is specific and is the useful part:
**the errors concentrated in the coordinator's own estimates and never in the
repository's state.** The repository is measurable by anyone; the coordinator's
arithmetic, memory and transcription are not, and every agent downstream of a
brief inherits them as premises.

#### Evidence

**PROVEN** for five falsified figures and one that verified. Each is cited to the
artifact that records it.

**(a) A change size, wrong in the alarming direction.** PR #643's size, measured
by three routes that agree:

```text
$ gh pr view 643 --json additions,deletions
additions=46  deletions=0
$ git diff --numstat 1cb61f3a 5d99a373            # merge base -> head
11	0	docs/approvals/APPROVAL_REGISTER.md
14	0	docs/evidence/documentation/acceptance-conversion-process-2026-10-02.md
21	0	docs/roadmaps/aegis-documentation-readability-backlog.md
$ git show d10f6319 --numstat --format='parent=%P'  # the squash commit against its parent
parent=e88a0a0d0691259745d20301d3f34b992cb8e1c4
(identical three lines)
```

`11 + 14 + 21 = 46` insertions and **0** deletions, and PR #643's own two review
records state the same (`5964118480` reads `+46/−0`; `5964119436` reads
`+46/-0`). The briefed coordinator figure for this change was **`+49/−3`**.
**That figure is false against three independent measurements of one object.**
The `+49/−3` value is itself `UNVERIFIED` as transmitted — a dispatch brief is
session state and no repository artifact records it — so what is PROVEN is the
measured `+46/−0` and that any `+49/−3` is wrong. Note what the false figure
asserts: **`−3` deletions** on a documentation-only append, the most alarming
possible misreading of this change.

**(b) A guessed count against a true set-difference.** PR #639's title reads
`chore(coord): append **three** evidenced coordinator idle-check entries`, and its
own diff is **four** insertions to the file it appends to:

```text
$ gh pr view 639 --json number,title,additions,deletions
title     = chore(coord): append three evidenced coordinator idle-check entries
additions = 4   deletions = 0
$ git show 6c4471b2 --numstat --format='subject=%s'
subject=chore(coord): append four evidenced coordinator idle-check entries (#639)
4	0	.coord/coordinator-cadence.jsonl
```

The commit subject, the diff and the byte-count chain all say **four**; only the
pull-request title says three. The count in the title was not taken from the diff.
This instance is recorded on the default branch independently of this page:
`.coord/coordinator-cadence.jsonl` line 20 raises it as a flagged judgment, and
PR #644's body states it too — *"PR #639's title says 'three' while its diff is
four insertions to this same file … and its commit subject says 'four'"*. Two
independent records of one arithmetic slip.

**(c) A self-audited figure, corrected by its own author.** PR #644's body carries
a revision note: *"Three defects in the earlier revision are fixed here: a false
figure ('19 of 23 lines carry `idle: null`' — the measured value is **14**), two
mis-transcribed key names … and a stale `origin/main`."* The measured value is
`14`, and the same body states it. A figure wrong by 5 of 23 was published in a
pull-request body and caught only by the author's own later audit — which is
precisely why `PROC-12` requires the **reader** to re-derive, rather than trusting
the author's audit of the author.

**(d) A brief's citation, falsified by grep.** PR #645's body records that
`source-of-truth-reconciler` resolved conflicts between the brief and the
repository, including *"that the brief's `Claude Agent SDK` citation for the
routing plan was wrong — grep exit 1 there, the exact phrase lives in
`aegis-setup-package-4b-host-proof-protocol.md`"*. The brief's citation resolved
to no file; the repository held the phrase elsewhere.

**(e) Time arithmetic, published into a tracked log.** The coordinator hand-typed
a poll window instead of measuring it, and the value went into
`.coord/coordinator-cadence.jsonl` as line 4. Measured:

```text
$ git log -1 --format='%cI' 914dcbb8              # the commit that added line 4
2026-10-02T00:37:32-07:00
$ <line 4's window end, parsed>
2026-10-02T08:25:00-07:00
$ delta
07:47:28
```

Line 4's window end is **7 h 47 min 28 s in the future** of the commit that
carries it. The defect was disclosed on PR #620 (`5947493567`: *"The coordinator
hand-typed the poll timestamps instead of measuring them, produced a series
roughly seven to eight hours in the future, and passed the wrong number to the
author as a fact"*), corrected forward by PR #621 and again by PR #622, and the
log's line 6 named the mechanism as *"a UTC hour … stamped with the local offset
-07:00"* — which **line 7 then withdrew as not reproducing**: applying that
mechanism to the cited instant yields `07:46:00-07:00`, 39 minutes short of the
value it was said to explain. The **magnitude is PROVEN**; the **cause is
unrecoverable**, and the log says so. This page repeats the log's own position
rather than the withdrawn one.

**(f) A figure that DID verify — recorded so the rule does not overreach.** The
briefed baseline of seven durations for the check that was called a stall
(`149 s, 151 s, 167 s, 216 s, 224 s, 227 s, 227 s`) **reproduces exactly** as
`tools-tests-windows` job durations in the sample measured in `7.5`, by the
job-level method. A rule that said "distrust every coordinator figure" would have
discarded a correct measurement. **The rule is re-derive, not disbelieve.**

**One count is deliberately not asserted.** The briefed claim is that roughly
**ten** coordinator figures were falsified across the session. **`UNVERIFIED`.**
This section evidences **five** (a–e) and one that verified (f); the count of ten
is session state with no artifact, and this page does not adopt it.

#### How it happened

Three causes, and only the first is about arithmetic.

1. **Estimates were produced where measurements were available.** `+49/−3` and
   "three" are each derivable in one command; both were stated from working
   memory of a diff.
2. **A brief is an unchecked channel.** A figure in a brief arrives as a premise.
   The agent on the other side has no marker distinguishing "the coordinator ran
   this" from "the coordinator believes this". `PROC-03` already requires the
   agent to re-derive briefed **gate conditions**; this section generalizes that
   to every briefed **number**.
3. **The coordinator is the one participant whose work leaves no diff.** Every
   agent's output is reviewable in the repository. The coordinator's arithmetic
   is not: it appears in briefs, which are session state, so a wrong figure has
   no artifact an auditor can read and no reviewer who sees it before it is used.
   The four figures in (a), (b), (c) and (e) survived to be caught **only**
   because they landed in a comment, a title, a pull-request body or a tracked
   log — the briefs themselves left nothing.

#### Standing rule — `PROC-12`

**Every brief must instruct the agent to re-derive the coordinator's numbers and
to say so when they disagree; and a coordinator figure offered without a command
is a claim like any other.** Concretely: a number in a brief is a **hypothesis**,
the agent's own measurement is the finding, and a disagreement is **recorded, not
silently reconciled** — the agent keeps its measured value and states the briefed
one beside it. A coordinator that states a figure it did not measure says so. And
the coordinator's estimates of **its own process** — "roughly ten figures were
falsified", how many dispatches returned nothing — are subject to this rule at
full weight: they are the least measurable claims in the session and they are
labelled `UNVERIFIED` in this class.

#### Detection check

For any figure about to be relied on, in the agent's turn:

```text
$ <the command that produces the figure>          # run it, do not recall it
$ <a second, independent route to the same figure>
```

Two routes, or the figure is a claim. For a **change size**, the two routes are
`gh pr view <n> --json additions,deletions` and
`git diff --numstat <merge-base> <head>`. For a **count of appended entries**, the
two routes are the title's claim and the diff's own `--numstat`. For an
**instant**, the two routes are the written value and
`git log -1 --format='%cI' <sha>` of the commit that carries it. A record that
states a briefed figure without its command fails this check.

---

### 7.7 — two live reviewers on one head

#### Issue

Two review dispatches overlapped at one head, so the pull request carries **two
independent review records for the same revision from the same identity**. It was
not harmful here — both records were accurate and agreed — but the failure mode
belongs in the register, because the same overlap on a **state-changing** verb is
`PROC-02` and `PROC-10`.

#### Evidence

**PROVEN.** PR #643 carries two review records bound to the same head
`5d99a373`, eight seconds apart, both returning `approve-with-nits`:

```text
$ gh api repos/ModernNomad-98/Project-Aegis/issues/comments/5964118480
created_at = 2026-10-03T01:29:39Z
  "CODE REVIEW — PR #643 … bound to head 5d99a373… (base: 1cb61f3a, 3 files, +46/−0)"
  verdict approve-with-nits
$ gh api repos/ModernNomad-98/Project-Aegis/issues/comments/5964119436
created_at = 2026-10-03T01:29:47Z
  "CODE REVIEW - PR #643, head 5d99a373… (base 1cb61f3a, 3 files, +46/-0)"
  verdict approve-with-nits
```

Both name `5d99a373`, both name the base `1cb61f3a`, and both return the same
verdict — so neither supersedes the other; they are two records for one head.
PR #645 carries the same shape: `5964180232` (01:37:59Z) and `5964191494`
(01:39:33Z), both bound to `3e509264`, 1 min 34 s apart.

The mechanism is already recorded on the default branch for a different artifact:
cadence log line 8 states the security review stage *"is now recorded twice on PR
#623 from the same identity"* because a record-posting agent was dispatched
without knowing another had already posted — and those two comments are
byte-identical (`5963358410`, `5963363229`; body SHA-256 `7080D2F7…`). **The same
defect, in a cheaper place and a more expensive one**: cheap on a comment, where
the cost is a duplicate record; expensive on a merge or a force-push, where the
cost is a second writer on a state-changing verb.

#### How it happened

Two dispatches were issued for one review, for the reason `7.4` gives: the
dispatch channel has no status, so "has the review been posted?" was answered by
re-reading the pull request, and the answer at the moment of the second dispatch
was **not yet**. Both agents then reviewed the same head correctly and the pull
request gained a second record. **Nothing in this repository refuses the second
record** — a comment has no uniqueness constraint — which is precisely why
`PROC-02` had to be written as a dispatch-time rule rather than left to a gate.

#### Standing rule — `PROC-13`

**One live reviewer per head.** Before dispatching a review, check whether a
review record already exists at the head being reviewed; if one does, the correct
actions are to **read it** or to **wait for it**, never to dispatch a second. A
record bound to an earlier head does not satisfy the check — a moved head voids
the earlier verdict, so a new dispatch is owed — which is the one case where a
second review of the same pull request is correct, and it is a second review of a
**different head**. Where two records do land at one head, they are **kept and
labelled, never deleted**: removing a governance record is worse than a
duplicate, which is the disposition the cadence log already recorded for PR #623.

#### Detection check

```text
$ gh pr view <pr> --repo ModernNomad-98/Project-Aegis --json headRefOid
$ gh api repos/ModernNomad-98/Project-Aegis/issues/<pr>/comments --paginate
```

Each of the six duplicate records, linked on one line so this repository's own
link checker can see it — see `7.3`(d) for why that qualification is not
decoration: [PR #643 comment 5964118480](https://github.com/ModernNomad-98/Project-Aegis/pull/643#issuecomment-5964118480), [PR #643 comment 5964119436](https://github.com/ModernNomad-98/Project-Aegis/pull/643#issuecomment-5964119436), [PR #645 comment 5964180232](https://github.com/ModernNomad-98/Project-Aegis/pull/645#issuecomment-5964180232), [PR #645 comment 5964191494](https://github.com/ModernNomad-98/Project-Aegis/pull/645#issuecomment-5964191494), [PR #623 comment 5963358410](https://github.com/ModernNomad-98/Project-Aegis/pull/623#issuecomment-5963358410), [PR #623 comment 5963363229](https://github.com/ModernNomad-98/Project-Aegis/pull/623#issuecomment-5963363229).

Count the comments whose body names the current `headRefOid` **and** carries a
verdict. **Two or more is the defect**, and the count is the dispatch decision:
`1` means do not dispatch, `0` means dispatch one and only one. Run it in the
**dispatcher's** turn — an agent cannot detect from inside its own turn that a
sibling is reviewing the same head.

---

### Honest limits of Class 7, stated with the class

- **Four of the seven defects cannot be evidenced from this repository, and this
  class says so at each one.** `7.1`'s dispatch counts, `7.2`'s push instant and
  second instance, `7.3`(a)'s historical measurement, and `7.4`'s second merge
  dispatch are session state. In every case the defect is **about an absence** —
  of an artifact, a timestamp, a record — and an absence leaves nothing to cite.
  That is not a gap in this page's research; **it is the defect.** A rule whose
  violation leaves no artifact can only be **prevented**, never detected after the
  fact, which is why six of these seven rules are dispatch-time rules.
- **`7.2`'s sweep is a negative result, not a clearance.** All 26 sampled session
  branches have a merged pull request today. The stranded state is transient, and
  this page cannot show it retrospectively.
- **`7.6`'s instance count is unverified.** The briefed claim is "roughly ten
  falsified figures"; this class evidences **five** and one that verified, and
  does not adopt the ten.
- **`7.5`'s stall run is unidentified.** The distribution and its method are
  measured; which run the conclusion was drawn about is not.
- **`7.3`(d) is a defect this class found in itself, and it is recorded at full
  weight.** The first version of this append wrapped its six links across a line
  break, the mandated checker could not see them, and the clean `broken: 0` was
  true only of the links it could see. The instance is listed as `PROVEN` because
  the fix moved the counts by exactly six — **and it is listed at all because a
  clean result that does not move when the input grows is the defect, not the
  pass.** It is left in the class rather than quietly fixed.

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
- **Class 7 added seven classes' worth of one mechanism, and four of its seven
  defects cannot be evidenced from this repository.** `7.1`'s dispatch counts,
  `7.2`'s push instant and second instance, `7.3`(a)'s historical measurement and
  `7.4`'s second merge dispatch are session state, because in each case the
  defect is *about an absence* and an absence leaves nothing to cite. **A rule
  whose violation leaves no artifact can be prevented but cannot be detected
  after the fact**, which is why six of the seven are dispatch-time rules. This is
  the same limit the third bullet above states for `PROC-02`, `PROC-03` and
  `PROC-06`, now measured on a larger sample: of thirteen rules on this page, ten
  are dispatch-time properties.
- **`PROC-08`'s sweep is a negative result, not a clearance.** All 26 remote
  branches whose tip commit falls in this session's window carry exactly one
  merged pull request, so no stranded branch is visible **now**. Stranded work is
  a transient state; the check is the deliverable and the sweep is not evidence
  that the defect never occurred.
- **`PROC-12`'s instance count is unverified.** The session's own claim is that
  roughly ten of the coordinator's figures were falsified; Class 7 evidences
  **five** and records **one that verified**, and does not adopt the ten. A rule
  that said "distrust every coordinator figure" would have discarded a correct
  measurement.
- **`PROC-05`'s correction and Class 7's `7.3`(c) are the same fact seen twice.**
  The link checker's absence from `main` at the time Class 5 was written is
  Class 5's UNVERIFIED figure; the link checker's absence from a **stale working
  tree** at a revision that predates it is `7.3`(c)'s reproduced exit 2. Neither
  is a claim that the checker is missing from the default branch — it is present
  there from PR #628's `b97ff272` onward.

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
| `PROC-04` (forbidden method) | `git grep 'Measure-Object -Line' -- '*.md'` returns hits that are all text *about* the trap. Mechanical only with an allowlist of pages that define the rule; without one it is a review prompt. | `scripts/` — gate-guard protected |
| `PROC-04` (method named) | Harder: requires parsing prose for a count and checking a method is named nearby. Heuristic, so advisory at best. | `scripts/`, advisory only |
| `PROC-05` (existence), partially | Fail when a tracked document cites a repository path that does not exist on the default branch. This would have caught reliance on `tools/readability_acceptance/`. A link checker of this kind now **exists on the default branch** — `scripts/ci/check-markdown-links.py` (PR #628, merged 2026-10-03T00:47:45Z) — so the earlier statement here that it was "unmerged, so it is not available and must not be relied on" is **corrected**: it is available at `origin/main` = `1cb61f3a`. It remains **not part of the required checks** this page can rely on, and adding it would still be a `scripts/` change costing a manual review, which is the point this section makes. | `scripts/` — gate-guard protected |

| `PROC-08` (stranded work), partially — **appended 2026-10-03** | For each recent remote ref, fail when `gh pr list --head <branch> --state all` is empty. This is a **complete** detector over the refs it reads, because the branch itself is the readable artifact. It needs `gh` authentication in the runner, which a hosted workflow does not have for this repository, so it is a **local cadence check**, not a workflow. | `scripts/` — gate-guard protected |
| `PROC-09` (existence by exit code) — **appended 2026-10-03** | Advisory only: a heuristic over prose for existence claims ("the file exists", "0 problems") that do not name an exit-code command nearby. Needs an allowlist of pages that define the rule, exactly as `PROC-04`'s forbidden-method grep does. | `scripts/`, advisory only |
| `PROC-13` (one live reviewer per head) — **appended 2026-10-03** | Fail a pull request that carries two or more verdict-bearing comments naming the same `headRefOid`. Every input is on the API; only the *classification* of a comment as verdict-bearing is a heuristic, and it can be narrowed to the record convention's own opening tokens. | `scripts/` — gate-guard protected |
**Not mechanically enforceable, and why:**

| Rule | Why not |
| --- | --- |
| `PROC-02` (review before merge dispatch) | Review records are plain issue comments, not GitHub review objects, because `gh` is authenticated as the PR author. A gate would have to classify comments by heuristic. It could be a **post-merge detection lane** comparing `mergedAt` to the earliest verdict timestamp, but a detection lane runs after the merge and cannot prevent one. |
| `PROC-02` (one agent per PR) | Agent dispatch is session state. No runner can see it. |
| `PROC-03` (re-verify briefed conditions) | A property of a brief's text and an agent's turn. Unrecorded in the repository. |
| `PROC-03` (record the measurement instant) | Checkable only by a reader of the record. A reviewer can enforce it; CI cannot. |
| `PROC-05` (re-derive from `main`) | Whether a conclusion was re-derived is a claim about process, not about bytes. Only the existence half is checkable. |
| `PROC-06` (re-dispatch check) | A runner sees no dispatch, so there is nothing for it to fail on: the check is five read-only commands a dispatcher must run in its own turn. Every input to it *is* observable — worktree, branch, remote ref, PR — but observability is not a gate, and no run of it can tell an early lane from a dead one (Class 6's honest limit). |

| `PROC-07` (mandatory deliverable) — **appended 2026-10-03** | Whether a dispatch named an artifact is a property of a brief's text, and whether an agent posted one is a property of a turn. The **consequence** is readable — an expected artifact is absent — but "absent" is indistinguishable from "never dispatched", which is the defect itself. |
| `PROC-08` (definition of done) — **appended 2026-10-03** | The push is readable; the **intent to propose** is not. A branch with no pull request is legitimate for a lane that never intended one, so a gate on "no PR" alone fails correct work. |
| `PROC-10` (addressable target) — **appended 2026-10-03** | Agent dispatch is session state. No runner sees a dispatch, a task board or a status, so there is nothing for it to fail on. |
| `PROC-11` (baseline before anomaly) — **appended 2026-10-03** | A runner can read the distribution; it cannot read that someone **called** an observation anomalous, because that call is a sentence in a report. |
| `PROC-12` (re-derive the coordinator's figures) — **appended 2026-10-03** | The brief is session state and the re-derivation is a property of a turn. A reviewer can enforce it; CI cannot. |
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

4. **`PROC-08` — a stranded-work sweep is owed, and it cannot be retrospective.**
   A sweep over the remote refs was run for Class 7 and found **no** stranded
   branch among the 26 session branches, which is a negative result: the state is
   transient and the sweep says nothing about earlier windows. The durable remedy
   is a cadence step, not a one-off sweep, and **this page's pull request adds
   neither**. **`PROC-11` — no maintained baseline table exists** for the
   durations of this repository's checks; the 13-run job-level sample in `7.5`
   was measured for Class 7 and is not kept anywhere, so the next agent that has
   to decide whether a check is slow will again have no baseline unless it
   re-measures. **`PROC-13` — the duplicate review records at PR #643's head and
   PR #645's head are left in place**, per the disposition already recorded for
   PR #623: removing a governance record is worse than a duplicate. **`PROC-12`
   — no home exists for the coordinator's figures.** A brief is session state, so
   a falsified coordinator figure leaves no artifact to correct and no page that
   owns it; this class records the five it could evidence and proposes no
   mechanism, because a mechanism would need a tracked home for briefs and that
   is a larger change than this append.
## Evidence summary

| Class | Claim | Verdict | Command |
| --- | --- | --- | --- |
| 1 | `65bacc7d6b85` is not an ancestor of `origin/main` | **PROVEN** | `git merge-base --is-ancestor 65bacc7d6b85 origin/main` → 1 |
| 1 | The object nonetheless exists in this mirror | **PROVEN** | `git cat-file -t 65bacc7d6b85` → `commit` |
| 1 | No ref reaches it; `rev-list --all` excludes it | **PROVEN** | `git for-each-ref --contains` → empty; `git rev-list --all` → absent |
| 1 | The false sentence entered with PR #626's squash commit `bff75d9c` | **PROVEN** | `git log -S "Each base SHA is the page's last recorded acceptance"` |
| 1 | PR #626's reviewed head `1e8b81e7` is also not on `main` (squash) | **PROVEN** | `git merge-base --is-ancestor 1e8b81e7 origin/main` → 1 |
| 2 | #626 and #627 merged with no review record in existence | **PROVEN** | `gh pr view <n> --json mergedAt,comments` |
| 2 | #623 carried **seven** comments before its merge: the Codex notice at 23:54:19Z plus **six** review records at six distinct timestamps (23:59:41, 23:59:54, 00:00:08, 00:00:39, 00:00:41, 00:00:42) — the three review **stages** named above (audit Audit-1 ACCEPT, readability REMEDY-1 SHIP, security) carried across six separate comments, two of them byte-identical (`IC_kwDOTPe6NM8AAAABY3Ggyg` / `IC_kwDOTPe6NM8AAAABY3GznQ`, SHA-256 `7080D2F7…`), **not** three records posted "once, twice and three times" | **PROVEN** | `gh pr view 623 --json comments,mergedAt` — 9 comments, 7 with `createdAt` < `mergedAt` 2026-10-03T00:01:15Z |
| 2 | #626's post-merge record returned FIX-FIRST on the Class 1 defect | **PROVEN** | comment body at `2026-10-03T00:13:01Z` |
| 3 | #624's head instant is 00:04:58Z; a Codex notice postdates it at 00:09:58Z | **PROVEN** | `git log -1 --format=%cI a0634422`; `gh pr view 624 --json comments` |
| 3 | The UNMET conclusion was measured at 00:09:47Z, 11 s before that notice | **PROVEN** | comment timestamps |
| 3 | What the coordinator's brief listed | **UNVERIFIED** | brief is a session artifact, not in the repository |
| 4 | True counts are 1492 / 1504; `Measure-Object -Line` gives 1319 / 1331 | **PROVEN** | raw `0x0A` byte count of each blob: `python -c "import subprocess;b=subprocess.run(['git','cat-file','blob','1b9e7049:docs/skills-catalog.md'],capture_output=True).stdout;print(b.count(b'\n'))"` → 1492, the same command at `93c0834f` → 1504; `(git show <rev>:docs/skills-catalog.md \| Measure-Object -Line).Lines` → 1319 / 1331 |
| 4 | The accusation was published and retracted | **PROVEN** | `gh api .../issues/comments/5963257423` and `/5963289254` |
| 4 | The join-and-split method over-reports by 1 **only on an unterminated blob**; splitting the **raw text** over-reports by 1 **unconditionally** | **PROVEN** | array form: `behavioral-eval-runner-wp-2b-0-finalization.json` 13 vs 12 (+1), `1b9e7049` 1492 vs 1492 (+0), `93c0834f` 1504 vs 1504 (+0); raw-text form: `(git show 1b9e7049:docs/skills-catalog.md \| Out-String).Split("`n").Count` → 1493 vs 1492, and 1505 vs 1504 at `93c0834f` (+1 at both) |
| 5 | PR #629 was open and its tool absent from `main` **when the figure was produced**; both facts are now false — it merged 2026-10-03T01:08:52Z and the tool is on `main` | **PROVEN** | then: `gh pr view 629` → `OPEN`; `git cat-file -e origin/main:tools/...` → 128. Now at `origin/main` = `1cb61f3a`: `state` = `MERGED`; same `cat-file -e` → 0; `gh pr view 629 --json files --jq '.files\|length'` → 13 (head `797ca687`) |
| 5 | The "159 no-record pages" figure | **UNVERIFIED** | not re-derived by this pass; the instrument is now on `main` (`tools/readability_acceptance/check_index.py`, `origin/main` = `1cb61f3a`), so re-derivation is possible, but this lane is barred from worktrees and helpers and no attempt was made |
| 6 | The seven→eight regression reproduces verbatim, and no source supports "eight" | **PROVEN** | `git show 4d08377d --numstat` → `1 1`; `rls-audit-checklist.md:35` = "Seven failure modes"; 7 numbered items; Workflow step 4 names 7 |
| 6 | The briefed "branch was NEVER pushed" is now **false**: the branch is on the remote at `145647cc` | **PROVEN** | `git ls-remote --heads origin`; `git merge-base --is-ancestor 4d08377d 145647cc` → 0; `git for-each-ref --contains 4d08377d` → 2 refs |
| 6 | The seven→eight regression is **discharged** by the owning lane at `145647cc`, not owed | **PROVEN** | `sed -n 218p` at `145647cc` and at `d9f57283` (`origin/main`), `sed -n 217p` at `5703e93f`: all three read "the seven failure-mode catalog" |
| 6 | Two dispatches put two writers on one worktree (`wt-ten`) | **UNVERIFIED** (the dispatch is session state; its consequence reproduces) | `git -C "C:\src\Project Aegis\wt-ten" reflog --date=iso`: 6 commits, one reset away, 5 surviving |
| 6 | A later `git worktree add` failed (exit 255) and the agent self-halted | **UNVERIFIED** (reported in a brief; a failed dispatch leaves no trace) | `git worktree list`: exactly one worktree per branch |

| 7.1 | PR #643's longest artifact-free interval is **8 min 31 s** (`5964045603` 01:21:08Z → `5964118480` 01:29:39Z); PR #645's is **3 min 10 s** inside a 5 min 15 s pull-request life | **PROVEN** | `gh api repos/ModernNomad-98/Project-Aegis/issues/643/comments` (10 comments, ids and instants listed); same for 645 (3 comments); `gh pr view 645 --json createdAt,mergedAt` |
| 7.1 | The tracked cadence log's last `checked_at` is `2026-10-02T18:18:37-07:00` and **four** merges landed after it | **PROVEN** | `git show origin/main:.coord/coordinator-cadence.jsonl` → 23 lines, 18 distinct `checked_at`; `gh pr view {633,643,644,645} --json mergedAt,mergeCommit` |
| 7.1 | That three review dispatches and one merge dispatch returned no artifact, that a comment count stayed flat, and that PR #645 needed a second merge dispatch | **UNVERIFIED** | session state; a silent dispatch leaves no ref, file, comment or log line, so the absence cannot be distinguished from an unrun dispatch |
| 7.2 | Branch `chore/cadence-log-append-3` exists on the remote at `0f62022d` and its only pull request is #644 | **PROVEN** | `git ls-remote --heads origin chore/cadence-log-append-3`; `gh pr list --head chore/cadence-log-append-3 --state all` → `#644 MERGED`, `createdAt` 01:26:49Z |
| 7.2 | The branch's **push instant**, and any second stranded instance in the session | **NOT DERIVABLE / UNVERIFIED** | `gh api repos/ModernNomad-98/Project-Aegis/events` → 52 `PushEvent`s, that ref absent; a 26-branch sweep finds every session branch proposed today |
| 7.3 | A **failed** `git show` emits one line of text while `git cat-file -e` exits **128** | **PROVEN** | `git show '6715cefc:scripts/ci/check-markdown-links.py' 2>&1` → 1 line, the `fatal:` text; `git cat-file -e` → 128 |
| 7.3 | The absent/present pair: `724644aa:docs/evidence/approvals/APPROVAL_REGISTER.md` → **128**; `5d99a373:docs/approvals/APPROVAL_REGISTER.md` → **0**, size **193671** | **PROVEN** | `git cat-file -e` and `git cat-file -s` on each |
| 7.3 | `1cb61f3a` resolves, is a `commit`, and **is** an ancestor of `origin/main` | **PROVEN** | `git rev-parse --verify 1cb61f3a`; `git cat-file -t` → `commit`; `git merge-base --is-ancestor 1cb61f3a origin/main` → 0, five consecutive runs |
| 7.3 | The mandated link checker is absent from the `coord-main` **working tree** and Python exited **2** with "can't open file" | **PROVEN** | `Test-Path` → False; `git cat-file -e 797ca687:scripts/ci/check-markdown-links.py` → 128; `python -B scripts/ci/check-markdown-links.py docs/` → exit 2. Present on `main`: `git cat-file -e 3c58e966:…` → 0; absent at `6715cefc`, `b0d3ab71`, `d9f57283` → 128; arrived at `b97ff272` → 0 |
| 7.3 | That a coordinator counted a failed `git show`'s error line as file content and reported a file present at exit 128 | **UNVERIFIED** | searched 138 issue comments on PRs #613–#646 and the scratch under `artifacts/coord/` for `does not exist in`, `fatal: path`, `can't open file`: only records using the **correct** method were found |
| 7.3 | A checker that reports `broken: 0` did not count six added links, because its `LINK` regex forbids newlines and the links were line-wrapped | **PROVEN** | `python -B scripts/ci/check-markdown-links.py docs/` returned identical `external-skipped: 1691` before and after six links were added; `grep -n '^LINK' scripts/ci/check-markdown-links.py` → `[^\]\n]`/`[^()\n]`; `grep -n 'for line_number, line in'` → per-line loop. Un-wrapping the links moved `external-skipped: 1691 → 1697`, exactly +6, while `links checked` stayed 2388 (correct: the external branch `continue`s before `counts['checked'] += 1`) |
| 7.4 | PR #643 has exactly one `merged` event, by a human account, and **zero** review objects | **PROVEN** | `gh api .../issues/643/timeline`; `gh api .../pulls/643/reviews` → 0; `gh pr view 643 --json mergedAt,mergedBy` |
| 7.4 | PR #623's security stage is recorded **twice**, byte-identically, 31 s apart | **PROVEN** | `gh api .../issues/comments/5963358410` and `/5963363229`, bodies equal, SHA-256 `7080D2F7E028EA1C8B4170021B882885AC69EAB0F7BFBF8FDD2037B439D33332`; disclosed on cadence log line 8 |
| 7.4 | That two merge agents ran on PR #643, the second finding it merged 11 s before its first command | **UNVERIFIED** | a second agent that correctly reports leaves the same repository state as no second agent |
| 7.5 | `tools-tests-windows` job duration over 13 sampled runs is **149-240 s**, and the briefed seven figures reproduce inside it | **PROVEN** | `gh api repos/ModernNomad-98/Project-Aegis/actions/runs/<id>/jobs` → `started_at`→`completed_at`, per run id and head SHA tabulated in 7.5 |
| 7.5 | Job-level and run-level duration differ for the same run: **149 s** versus **232 s** | **PROVEN** | same `/jobs` command against `gh run list --json databaseId,createdAt,updatedAt` for run `37084966265` |
| 7.5 | Which run was called a stall, and the two polls that called it so | **UNVERIFIED** | a poll is session state; no poll log for it is tracked |
| 7.6 | PR #643 is **`+46/−0`** by three independent routes, not `+49/−3` | **PROVEN** | `gh pr view 643 --json additions,deletions` → 46/0; `git diff --numstat 1cb61f3a 5d99a373` → `11+14+21 = 46`, 0 deletions; `git show d10f6319 --numstat` → identical; both review records state `+46/−0` |
| 7.6 | PR #639's **title** says three while its diff is **four** insertions | **PROVEN** | `gh pr view 639 --json title,additions` → "three", `additions=4`; `git show 6c4471b2 --numstat` → `4 0`; also recorded on cadence log line 20 and in PR #644's body |
| 7.6 | PR #644's body records a false figure `19` corrected to the measured **`14`** | **PROVEN** | `gh api repos/ModernNomad-98/Project-Aegis/pulls/644` body, revision note |
| 7.6 | A brief's `Claude Agent SDK` citation for the routing plan resolved to no file | **PROVEN** as recorded | PR #645 body, quoting `source-of-truth-reconciler`'s resolution against the repository |
| 7.6 | Cadence log line 4's window end is **7 h 47 min 28 s in the future** of the commit that carries it | **PROVEN** | `git log -1 --format='%cI' 914dcbb8` → `2026-10-02T00:37:32-07:00`; the written value `2026-10-02T08:25:00-07:00`; `delta = 07:47:28` |
| 7.6 | That "roughly ten" coordinator figures were falsified | **UNVERIFIED** | five falsified figures and one verified figure are evidenced in 7.6; the count of ten is session state and is not adopted |
| 7.7 | PR #643 carries **two** `approve-with-nits` records at head `5d99a373`, 8 s apart | **PROVEN** | `gh api .../issues/comments/5964118480` (01:29:39Z) and `/5964119436` (01:29:47Z); both name head `5d99a373` and base `1cb61f3a` |
| 7.7 | PR #645 carries **two** records at head `3e509264`, 1 min 34 s apart | **PROVEN** | `gh api .../issues/comments/5964180232` (01:37:59Z) and `/5964191494` (01:39:33Z) |
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

**Provenance (Class 7) — appended 2026-10-03.** Evidence for Class 7 was gathered
read-only from the linked worktree `C:\src\Project Aegis\coord-main`
(`git rev-parse --git-dir` returns
`C:/src/Project Aegis/Project-Aegis/.git/worktrees/coord-main`, one shared object
store with every lane) at a re-fetched `origin/main` =
`3c58e9668d137e6bba69de3bc2ef6b73e542e76a` — the exact base revision this append
is committed on — plus the GitHub API as `ModernNomad-98`, on 2026-10-02/03.
Nothing was measured from the stale root checkout `Project-Aegis`, and **no
tracked content was read from the `coord-main` working tree**: every tracked
figure is from `git show <rev>:<path>` or `git cat-file`, which is why `7.3`(c)
is reported as an observation about that working tree and explicitly **not** as a
fact about the default branch. The `tools-tests-windows` durations in `7.5` are
**job-level** (`started_at` → `completed_at`) and are labelled so, because the
run-level route gives different numbers for the same run. Every line count in
Class 7 is a **newline count**, being the number of `0x0A` bytes in the raw blob;
every change size is from `git diff --numstat` and is stated as added + deleted.
`Measure-Object -Line` was not used, and PowerShell `>` was not used to materialise
a blob (the byte-level comparisons in this append used `cmd /c` redirection and
`[System.IO.File]::ReadAllBytes`, as `PROC-04` requires). No provider or model
call was made. Six claims in this class are labelled `UNVERIFIED` where they
appear, and `7.2`'s push instant is labelled **NOT DERIVABLE**; the count of
"roughly ten" falsified coordinator figures is recorded as an unverified claim
rather than adopted. **Skills applied:** `source-of-truth-reconciler`, for
resolving the disagreements between the dispatch brief and the repository — the
file's own `—` heading convention over the template's `:`, the repository's
measured `+46/−0` over a briefed `+49/−3`, the file's append-only practice over
in-place correction, and the register's own precedent (PR #633, which left
`docs/roadmaps/aegis-open-decisions-2026-09-23.md` untouched) over adding a dated
note there — and `lane-authoring-guide`, for keeping this to one lane and one
unit of work, citing every load-bearing claim or labelling it `UNVERIFIED`, and
recording explicitly what this append did **not** touch.
