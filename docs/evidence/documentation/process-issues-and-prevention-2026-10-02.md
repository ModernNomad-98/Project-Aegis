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
| `PROC-01` | For a declared list of (SHA, claim) pairs in the tracked text, fail when `git merge-base --is-ancestor <sha> origin/main` exits non-zero. Needs a machine-readable list, which does not exist yet. **Corrected 2026-10-03:** a machine-readable, revision-keyed list **does** exist on the default branch — `tools/readability_acceptance/acceptance-index.json` (350,376 bytes; 602 `reader_pages` rows, 443 of them carrying a `last_acceptance_sha`, plus an `acceptance_reachability` block whose probe is `git for-each-ref --contains <sha> --format=%(refname) refs/remotes/`, 7 rows annotated, 2 unreachable revisions). It landed as PR #629 at `1cb61f3a` (2026-10-02T18:08:51-07:00), **before** this page's own PR #633. What is still absent is a list **declared for this gate** pairing each SHA with its **claim**: the index pairs a SHA with its **page**. Measured at `origin/main` = `d9db0b83`. | `scripts/` — gate-guard protected |
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

5. **`PROC-11` and `PROC-12` are DISCHARGED — appended 2026-10-03.** The tracked
   home that item 4 recorded as missing now exists:
   [coordinator figures and the check-duration baseline](../../roadmaps/aegis-coordinator-figures.md).
   It is the tracked home for the coordinator's figures (`PROC-12`) and it
   carries the maintained job-level check-duration baseline (`PROC-11`) as its
   first landed figure set, so the two owed items are discharged by **one**
   artifact rather than two. The page states the rule that makes the home worth
   having: a figure supplied in a brief is a **claim**, and it enters the page
   only after being re-derived with its own query and recorded with the
   command, the revision and the date beside it — or else recorded as
   `unknown`. **The baseline was independently re-derived before it was
   landed.** All five job rows matched the handed-over measurement exactly:
   `validate-skills` 296 / 18 / 104 / 114 / 164 (healthy floor 62 s; the 18 s
   minimum is the single failed job's early abort), `windows-offline-checks`
   296 / 129 / 220 / 238 / 412, `tools-tests-linux` 296 / 89 / 148 / 162 / 379,
   `tools-tests-windows` 296 / 120 / 222 / 239 / 277, `gate-guard`
   191 / 4 / 6 / 8 / 45 — as did the 105-of-296 `skipped` count for
   `gate-guard` on a `main` push, which is expected and is not a failure. The
   `tools-tests-windows` band check also reproduced: **260 of 296 runs
   (87.8 %)** fall inside the previously claimed 149–240 s band, and that band
   **contains the 222 s median**, so the earlier "stalled job" alarm raised
   inside it was false by construction. **One figure disagreed and the
   measurement was landed, not the prose:** the workflow-level p90 is
   **258 s**, which is also what the first measurement's own machine-readable
   output recorded, against **257 s** written in its report prose. That row is
   the workflow-level contrast quantity, which the page forbids using to judge
   job stalls; the discrepancy is recorded on the page (§5) rather than
   silently repaired. **What this append does not claim:** it does not
   re-audit or correct any figure in `7.5`, whose 13-run sample the new
   baseline **supersedes rather than corrects**; it adds, renumbers and
   rewrites no class, rule or earlier owed-work item; and the new page is a
   **new tracked page and starts `pending`**, because the targeted-edit rule
   *retains* an acceptance and cannot confer one, so it owes an independent
   full-page re-read by a reader who did not write it. No tracked home yet
   exists for coordinator figures of any kind other than check durations; that
   remaining gap is stated on the page as its honest limit 1.

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


---

## Appended 2026-10-03 (second append) — `PROC-14` added, the `PROC-04` and `PROC-08` owed halves landed, PR #649's follow-up recorded

This append is **pure addition**. It changes no earlier line, renumbers no class
and rewrites no rule: items 1–5 of the owed-work list and the Class 7 table's
rows `7.1`–`7.7` are left exactly as written, and the new Class 7 row is
recorded here as `7.8` rather than inserted into a table above.

### Standing rule — `PROC-14`

**A history query run from a worktree whose `HEAD` is DIVERGENT from the default
branch silently omits every commit that HEAD cannot reach, so an empty result is
not evidence of absence. Name the ref.**

`git log`, `git log -S`, `git log -p`, `git log --follow` and their family
default to `HEAD`. When the worktree's `HEAD` is *behind* the default branch,
that default omits the newer commits. When it is **divergent** — neither an
ancestor nor a descendant of the default branch — it omits them too, and the
worktree shows no other sign of trouble. The failure is silent in the direction
that matters: the query **succeeds** (exit 0) and prints nothing, which reads as
"this text never changed" rather than "this revision cannot see it".

**Why this is not `PROC-01`.** `PROC-01` tests an ancestry claim you already
hold. This register already records `797ca687` as not an ancestor of
`origin/main`, and `7.3`(c) records the checker being absent from the
`coord-main` **working tree**. Both are about a *fact you have been given* or a
*tree's contents*. Neither states the trap here, which is a property of the
**query default**: it bites a query you have not yet run, on a tree that looks
healthy, and it returns a confident empty answer. `PROC-14` is therefore new,
not a duplicate. Verified by grepping this page before adding it: `divergent`
has **zero** hits, and the only `797ca687` hits are the Class 5 correction,
`7.3`(c) and the item-5 row — none of which makes this claim.

**Measured instance, re-derived 2026-10-03.** `C:\src\Project Aegis\coord-main`
is a linked worktree. Every figure below was re-derived at
`origin/main` = `bd622661fe56779227887cbd390eaeab9dfb37fd`, the tip current when
this correction was written:

| Check | Command | Result |
| --- | --- | --- |
| Worktree HEAD | `git -C … rev-parse HEAD` | `797ca687c58a059f76b585993cbd72032bc33c88` |
| Merge base | `git merge-base 797ca687 origin/main` | `d6e484189cc30c67dc69aeb973e15f89b693537d` |
| HEAD an ancestor of main? | `git merge-base --is-ancestor 797ca687 origin/main` | exit **1** — no |
| Main an ancestor of HEAD? | `git merge-base --is-ancestor origin/main 797ca687` | exit **1** — no, so the pair is **DIVERGENT** |
| Commits main has that HEAD cannot reach | `git rev-list --count 797ca687..<tip>` | **a SERIES, not a number** — see below |
| Commits HEAD has that main lacks | `git rev-list --count <tip>..797ca687` | **2** (`797ca687`, `7c52b6f6`) |

**The unreachable-commit count is published as a series, because a single
integer beside a named tip decays the moment `main` moves.** Measured with the
same counted command, one row per tip:

| `origin/main` tip | what landed | `git rev-list --count 797ca687..<tip>` |
| --- | --- | --- |
| `279ac94d` | the tip the original brief measured | **25** |
| `9f5dc6b3` | +#650, the figures page | **26** |
| `20fadd48` | +#648, the wrapped-link fix | **27** |
| `25cc0e7a` | +#649, the link-checker self-tests | **28** |
| `bd622661` | +#652, APR-103/104 | **29** |

The merge base (`d6e48418`), the two ancestor-test exit codes, and the reverse
count (**2**) are stable across all five tips; only the forward count moves,
because it counts commits on `main` that `HEAD` cannot see. `HEAD` is frozen, so
`main`'s growth is the only variable.

**Correction, recorded rather than silently repaired.** An earlier revision of
this append published **26** beside the named tip `25cc0e7a`. That was wrong by
two: 26 is the value at `9f5dc6b3`, and the value at `25cc0e7a` is **28**. The
cause is exactly the failure `PROC-04` forbids — a figure measured at one
revision and published beside another, because `main` advanced twice between the
measurement and the write-up. The **argument** that append made was right and is
kept: the count is revision-bound, and the brief's 25 was true at `279ac94d`.
Only the published figure was wrong, and it is now a series so that it cannot
decay again. A reviewer measured it moving 28 → 29 inside a single review window,
which is why a bare corrected integer would have re-opened this defect.

The false-empty instance, reproduced:

```text
$ git -C "C:\src\Project Aegis\coord-main" log -S "Consistency note 2026-10-02" \
    -- docs/roadmaps/aegis-open-decisions-2026-09-23.md
                                  # no output, exit 0  -- FALSE EMPTY
$ git -C "C:\src\Project Aegis\coord-main" log origin/main \
    -S "Consistency note 2026-10-02" -- docs/roadmaps/aegis-open-decisions-2026-09-23.md
3c58e966 docs(approvals): record AEGIS-APR-102 for the integration roadmap policy (#645)
```

**Detection check.** Before trusting any empty history result, ask whether the
ref was named:

```text
$ git merge-base --is-ancestor HEAD origin/main \
    || echo "HEAD is NOT an ancestor of origin/main: name the ref in every history query"
```

A non-zero exit means every `git log`-family call in that worktree must name
`origin/main` (or the specific revision) explicitly. The check is one command
and is cheap enough to run whenever a history query is about to decide anything.

**What this rule does not cover.** It does not tell you which ref to name when
the answer you want is genuinely about a branch's own history, and it does not
detect a *behind-but-not-divergent* HEAD, where the same silent omission occurs
for a smaller set of commits. Both need the ref named; neither is a gate, and no
script here enforces it — a runner cannot see which ref a reader intended.

### Class 7 row `7.8` (appended, not inserted)

| # | Claim | Verdict | Command |
| --- | --- | --- | --- |
| 7.8 | `git log -S` with no ref, run from the divergent `coord-main` worktree, returns a FALSE EMPTY for text that `origin/main` carries | **PROVEN** | `git log -S "Consistency note 2026-10-02" -- docs/roadmaps/aegis-open-decisions-2026-09-23.md` → no output, exit 0; the same query with `origin/main` named → `3c58e966` |
| 7.8 | That worktree HEAD is divergent from `origin/main`, not merely behind: neither is an ancestor of the other | **PROVEN** | `git merge-base --is-ancestor 797ca687 origin/main` → 1 **and** `… origin/main 797ca687` → 1; merge base `d6e48418` |
| 7.8 | Main carries **29** commits unreachable from that HEAD at `bd622661`, and HEAD carries **2** that main lacks; the forward count is a **series** (25 / 26 / 27 / 28 / 29 at `279ac94d` / `9f5dc6b3` / `20fadd48` / `25cc0e7a` / `bd622661`) | **PROVEN** — forward count by `git rev-list --count 797ca687..<tip>`, series re-derived 2026-10-03 at `origin/main` = `bd622661` | `git rev-list --count 797ca687..bd622661` → **29**; `git rev-list --count bd622661..797ca687` → **2** |
| 7.8 | *(superseded, kept for the record)* The same count published as the bare integer **26** beside `origin/main` = `25cc0e7a` | **FALSIFIED** — 26 is the value at `9f5dc6b3`; the value at `25cc0e7a` is **28** | `git rev-list --count 797ca687..25cc0e7a` → 28 |

### `PROC-04` — the owed writing-standards half is LANDED

Item 3 above recorded that the rule "belongs in the repository's documentation
standards, which this PR does not edit." It is now edited, and the location was
chosen from the repository's own text rather than by preference:

- The [documentation readability backlog](../../roadmaps/aegis-documentation-readability-backlog.md)
  plan item 4 says to "**add a short writing standard to the contribution
  guide** and check new or changed documentation against it in review."
- `CONTRIBUTING.md` already carries that guide as
  `## Write documentation for a new reader`, a numbered list of documentation
  rules that this rule extends as **item 7**.
- `docs/skill-generation-standard.md` was rejected: it is scoped to skill
  authoring contracts, not to documentation prose. `AGENTS.md` was rejected for
  this rule: the recommendation paragraph for `AGENTS.md` above
  reserves that file for the two **dispatch-time** rules (`PROC-02`
  concurrency, `PROC-03` re-verification), and a line-count rule is a writing
  rule.

The landed text carries all four clauses this register's `PROC-04` requires: a
count must name its method; a line count is a **newline count** and
`Measure-Object -Line` is forbidden for it because it drops blank lines; a
trailing-newline change must be checked explicitly because it moves a length by
one; and a change size comes from `git diff --numstat` or a genuine ancestor
range, never a two-dot diff between unrelated tips, which reports unrelated
files as deleted.

**The forbidden-method grep is unchanged and still a review prompt, not a gate.**
Its hit list is a revision-bound figure and gains this page's own wording once
this change merges, exactly as `PROC-04`'s detection check already predicts.

### `PROC-08` — the owed cadence step is LANDED

Item 4 above recorded that "the durable remedy is a cadence step, not a one-off
sweep, and this page's pull request adds neither." It is now landed where this
repository records its cadence: **one appended line in
`.coord/coordinator-cadence.jsonl`**, the log whose own `_comment` defines the
schema and states that the file is append-only and hand-maintained.

The step is the detector this page already designed in its "Mechanically
enforceable, and where it would live" table: for each recent remote ref, fail
when `gh pr list --head <branch> --state all` is empty. It is a **local**
cadence check, not a hosted workflow, because a hosted runner has no `gh`
authentication for this repository. **The detector is complete over the refs it
reads** — the branch itself is the readable artifact, so an empty result is a
real finding, unlike `PROC-07`'s silent dispatch, whose absence cannot be
distinguished from an unrun dispatch. It cannot be retrospective: it reports the
state at the instant it runs, which is precisely why the remedy is a cadence
step.

**Append-only, proven by hash.** The pre-edit blob is
`5cf558227062143505ed65797b585cfa53acdeaf` (20 507 bytes, **23** newlines,
terminated). The post-edit file is 21 486 bytes and **24** newlines; the
pre-edit bytes are an exact byte **prefix** of the post-edit file, the newline
delta is exactly 1, and every pre-existing JSON line still parses.

**Separator style corrected in review.** The appended line first used
`json.dumps` defaults, which emit a space after every `:` and `,`; the file's
other 23 lines are compact. This was raised as a `[NIT]` by the independent
review and is fixed rather than declined: line 24 now round-trips
compact-identically (7 bytes smaller, 21 493 → 21 486), its recorded
`checked_at` and text are unchanged, and the append-only proof above still
holds against the same base blob. The line's action text contains one `": "`
of its own prose, which is content, not a separator.

### PR #649 — the declined `[NIT]` follow-up is now RECORDED

`PR #649`'s reviewer (comment `5966277042`) found the declined `[NIT]`
"— the checker is invoked by no workflow step over the repository's own
Markdown —" was *declared* in the pull request body ("left for its own work
item") but **never recorded**: there is no matching open issue, and this
repository has exactly one open issue (#101, unrelated). The follow-up is
recorded here, with the two facts its record was missing, both re-derived at
`origin/main` = `bd622661fe56779227887cbd390eaeab9dfb37fd`:

1. **The named fix would fail CI as written.** The checker's **default scope is
   every tracked `.md` file** — 673 of them now. Run with no arguments at this
   revision it exits **1**:

   ```text
   files: 673   links checked: 3184   anchors checked: 800   broken: 6   dead: 1
   external-skipped: 1791   other-skipped: 0
   ```

   **All seven findings (six broken, one dead) lie inside the checker's own
   deliberately-broken test fixtures** under `scripts/tests/fixtures/` — the
   `markdown-links/bad/`, `paths-tree/` and `contract-audit/` trees. **None is a
   real repository link.** Over `docs/` alone the same checker reports
   `broken: 0, dead: 0`, exit 0. So the follow-up is not a one-line step
   addition: any wiring must first exclude the fixtures.
2. **The checker exposes no exclusion flag.** Its interface is `paths`
   (positional, default every tracked `.md`), `--root`, `--quiet` and `--json` —
   verified from its `argparse` block at blob
   `efa65c95f5444e50867e832a688c8351cd332d2c`. An exclusion therefore needs
   either a new flag in `scripts/` or an explicit path list.

**Status at this revision.** The *self-test* half of the original defect (C1b)
is closed: PR #649 merged as `25cc0e7a` and now runs
`scripts/tests/test_markdown_links.py` in **both** gate jobs
(`.github/workflows/validate-skills.yml:129` and `:227`). What remains open is
the checker **itself** never being run over this repository's own Markdown, so a
broken relative link can still merge green. That is a different defect from
C1b, it needs a `scripts/` or `.github/` change, and it is **owed**.

### What this append does not claim

It does not re-derive or correct any earlier figure in this page, and it does
not renumber, rewrite or annotate items 1–5; where an owed item is now
discharged, that is stated here and the original text is left standing. It adds
no gate: `PROC-14` and the `PROC-08` cadence step are rules an agent follows, and
the register's own mechanically-enforceable table still lists the `PROC-08`
detector as living in `scripts/`, which this change does not touch. It does not
claim the cadence log's new line has ever been *executed* — it records the step,
not a run of it.


## Appended 2026-10-03 (third append) — the `AGENTS.md` placement instruction corrected forward

This append is **pure addition**. It changes no earlier line, renumbers no class
and rewrites no rule. The paragraph it corrects — the `AGENTS.md` recommendation
at lines 2094–2104 — **stands exactly as written**, and is corrected here rather
than edited, because this page's own practice is to correct forward rather than
rewrite a dated measurement and because `CONTRIBUTING.md` rule 4 makes the same
requirement of recorded decisions.

### The instruction that was wrong, quoted

The paragraph directed *where* the two dispatch-time rules should go, and its
final sentence carried both the method and the claim that the method works
(lines 2101–2102), verbatim:

> Extending those sentences would place the rule where the coordinator reads it.

**The how and the purpose are in one sentence, and the sentence asserts that the
how achieves the purpose. Measurement falsifies that assertion** — so the *how*
was followed and the *purpose* was still not met. This is recorded as a
correction to an instruction, not as a defect in the rule it directed: both
rules were placed, and both bind.

### Why the instruction was wrong

`AGENTS.md` has **12 paragraphs**, of which **5 open with a bold span**. That
paragraph-initial bold lead is the file's only rule-discovery convention — it is
how `**Determine workspace role before acting.**`,
`**Audit your own state; assume nothing about your own work.**` and
`**Source-library owner approvals.**` are found by a reader scanning the file.
The file has one heading in total, so no heading reaches a rule either.

Extending the two sentences placed both rules **inside one paragraph** — the
4,062-character coordinator paragraph that opens
`**Coordinator role: assign, verify and hand off — do not perform the work.**`
Neither rule opened a paragraph:

| Rule | Position in that paragraph | Sentences before it |
| --- | --- | --- |
| `PROC-02` concurrency | offset **1,479** of 4,062 | **5** |
| `PROC-03` re-verification | offset **2,662** of 4,062 | **8** |

**A reader scanning for paragraph-initial bold — the file's own convention —
reached neither rule.** The rules were in the file and were not findable by the
method the file teaches. That is the gap this correction closes.

### Standing instruction, corrected

**A dispatch-time rule reaches the coordinator only when it OPENS its own
paragraph with a bold lead — that paragraph-initial bold span is this file's
discovery convention. Extending an existing sentence is necessary but NOT
sufficient: extend the sentence, and give the rule its own paragraph.**

A rule that is merely appended to a long paragraph is present and unfindable.
When placing a rule in `AGENTS.md`, verify the placement the same way as the
placement of a rule anywhere else — **by looking for it with the method a reader
would use**, not by confirming the words are present. Presence is not
discoverability, and only the second one is the purpose.

### One consequence for the same rule's wording

A rule given its own paragraph must also **open with a self-contained sentence**.
A paragraph break puts the previous paragraph's antecedent out of reach: an
opener such as *"The same holds for every other condition a brief asserts"*
still binds, because its own clause states the rule in full, but it now reads as
a continuation of a sentence the reader has left behind. The rule as landed
therefore opens
`**A brief's assertion of a gate condition is a claim, not evidence — of any condition, not only of authority. …**`
— self-contained, so the paragraph stands alone.

### What this append does not claim

It does not re-derive, contradict or renumber anything else on this page, and it
does not touch items 1–5 of the owed-work list, the Class 7 table, or the second
append above; the corrected paragraph at lines 2094–2104 is left byte-identical.
It records no new rule ID: the corrected text is an instruction about *placement*,
and `PROC-02` and `PROC-03` are unchanged. It does not claim the placement defect
was a failure of the rule or of its author's reading — the instruction itself was
followed, and the instruction was what measurement contradicted. It does not
claim that paragraph-initial bold is enforced: no test reads paragraph shape, and
this correction is a rule an agent follows rather than a gate that fails.

---

## Appended 2026-10-03 (fourth append) — `Q1`: the `PROC-02` sweep is DISCHARGED

This append is **pure addition**. It changes no earlier line, renumbers no class and rewrites no
rule: owed-work items 1–5 above are left exactly as written, and item 2 — *"`PROC-02` — a sweep is
owed"* — is discharged **here**, so that the discharge and the owed item are both readable without
either being rewritten.

**Why an append and not a new file.** Item 2 is a debt this page records, in this page's own
list; a discharge filed elsewhere would leave the debt and its settlement in two places, which is
the split that made the first sweep invisible in the first place. Before this append,
`git grep -l 'PROC-02' origin/main` returned **exactly one** tracked file — this page — so the
sweep existed as a claim about a measurement and not as the measurement. That is the `PROC-12`
failure mode this register names.

**Revision history of this block.** Four review passes corrected it before it merged, and every
correction is stated where it applies rather than hidden. A stated **reason** for the inline
endpoint's zero that was false by 191 rows; a **zero-match count** computed under two different
patterns and printed as two different numbers; an **unpublished verdict-token set**; a **receipt
limit**; a **findings heading** that asserted all of its rows were review records; and, in this
pass, the four corrections in the section immediately below. Every pattern is given verbatim so
that every count in this append reproduces from the commands and the patterns alone.

### The instrument turned on itself, and that is part of the result

This append exists to catch claims that outrun their evidence. **It made three of them, and two
different reviews caught them.** The first — a *reason* for a zero that was false by 191 rows —
was caught by the **independent human review** at comment `5972227605`. The other two — that this
append's own supporting commands' outputs were quoted, and that this repository has no formal
review objects — were caught by **`chatgpt-codex-connector[bot]`**, in inline findings
`4174407637` and `4174407642`, both filed `2026-10-03T18:51:17Z`. Two of the three are the
identical failure — **a claim about its own evidence that its own text does not support** — which
is the failure the whole page is about.

I am recording that here rather than quietly fixing it, for one reason a reader needs: **the
counts below were produced by an instrument that was wrong four times, so they should be read
with the corrections visible rather than trusted because they are printed.** That is also the
strongest evidence for this register's own thesis — the errors were found by an independent
reviewer re-measuring, not by the author re-reading, and the same is true of every finding below.

### Scope

**Every merged pull request in this repository's history**, from the first to the latest,
enumerated in one paginated sweep rather than sampled. The window is published as a **series**
for the reason the `PROC-14` append above gives for its own count: a single integer beside a
moving `main` decays the moment another PR merges, and the corpus of comments grows with every
cycle.

| measurement | merged PRs | latest `mergedAt` in the window | comment rows found | PRs found |
| --- | --- | --- | --- | --- |
| the session that ran the first sweep | 634 | `2026-10-03T02:16:17Z` | 23 | 20 |
| the first draft of this append | 639 | `2026-10-03T06:56:24Z` | 28 | 25 |
| this revision's earlier measurement | 640 | `2026-10-03T18:09:29Z` | 29 | 26 |
| **this revision** (corpus closed at the newest comment, `2026-10-03T21:23:54Z`) | **641** | **`2026-10-03T21:17:59Z`** | **27** | **27** under the per-comment rule; **15** under the register's own detector |

The window opens at the repository's earliest merged pull request, #1, `2026-07-06T19:06:52Z`;
there is nothing before it to cover. Completeness was cross-checked against `gh pr list --state
all`: **658** pull requests = **641 merged + 4 open +
13 closed-unmerged**, so the merged enumeration is whole and no pagination was lost.

**The rows are measurements, not corrections of one another.** The counts move because the corpus
moves: merges and comments landed between measurements, and one of those merges — #653 — is
itself a finding here, its review record posting 40 seconds after it merged. Earlier figures are
left standing as their own rows rather than overwritten, which is the same practice this page
applies to its own superseded counts.

### Method — the exact commands, the published patterns, and the two definitions of a finding

Both corpora are fetched **in bulk**; no call is made per pull request.

```text
$ gh pr list --state merged --limit 1000 \
    --json number,title,mergedAt,headRefOid -R ModernNomad-98/Project-Aegis
$ gh pr list --state all    --limit 1000 --json number,state \
    -R ModernNomad-98/Project-Aegis
$ gh api --paginate --slurp "/repos/ModernNomad-98/Project-Aegis/issues/comments?per_page=100"
$ gh api --paginate --slurp "/repos/ModernNomad-98/Project-Aegis/pulls/comments?per_page=100"
```

**One more method check, from the same sweep, because a cap and a pagination are different
claims.** The two `gh pr list` calls use `--limit 1000` — a **cap**, not pagination — and a cap that
is reached truncates silently. It is **not** reached: the enumeration returns **658** pull requests
and the API's own `Link: rel="last"` total for `/pulls?state=all` is **658**, so the merged
enumeration (**641**) is complete. The comment corpora were checked the same way — their
`Link: rel="last"` totals matched the rows fetched — which is how the `#77` pagination artifact
below was found and how its neighbours were cleared.

**A review record is a posted pull-request comment — but this repository does have formal review
objects, and an earlier draft of this append said it did not.** That was false. Measured, with
pagination, which is the whole point here:

```text
$ gh api --paginate --slurp "/repos/ModernNomad-98/Project-Aegis/pulls/<n>/reviews?per_page=100"
  #77 -> 83    #653 -> 7    #654 -> 2    #29 -> 1
  #650 -> 0    #623 -> 0    #611 -> 0    #213 -> 0    #2 -> 0
```

**The first draft of this paragraph published `30` for #77, and that was a pagination artifact.** A
bare `GET /pulls/77/reviews` returns GitHub's **default page of 30**; `per_page=100` with
`--paginate` returns **83**. The figure is corrected and the command is published beside it,
because a count produced by a truncated method is precisely what `PROC-04` governs — the same
requirement this append already meets for its comment corpora, so publishing `30` was also
inconsistent with its own method. **Every other review-object count in this append was re-checked
the same way and none moved**, because `7`, `2`, `1` and the zeros are all below the default page
size and the cap could not have hidden anything. What is actually true is narrower, and is what the
method depends on:
**on the pull requests whose review record is an issue comment, `reviews` comes back empty** —
measured `0` on #650, #623, #611, #213 and #2 — while the pull requests that *do* carry review
objects are the ones where the Codex bot submitted an inline review. The empty list is real; the
generalisation was not. The reason the distinction matters is that the records this sweep counts
are issue comments, and `gh pr view <n> --json reviews` is therefore not the query that finds them.

**Two definitions of "a finding", both published because they legitimately differ.**

1. **The per-comment rule (A)** — a pull request is a finding if **any** comment matching the
   record pattern has `created_at` **strictly greater than** its `merged_at`. This was the
   original definition of this sweep.
2. **The register's own after-the-fact detector (B)** — this page, `PROC-02`, immediately above:
   *"For the after-the-fact version, compare `mergedAt` against the **earliest** comment timestamp
   whose body contains a verdict"* and *"If `mergedAt` precedes the earliest review-record
   timestamp, that merge gated nothing."* Under B a pull request is a finding only when its
   **earliest** matching comment postdates the merge.

**A is a strict superset of B.** Measured at this instant: **27 pull requests under A,
15 under B**, and **every B finding is also an A finding** (the reverse set is empty). The
difference is **12 pull requests** — 7 merge receipts and 5 records that
quote or supersede an earlier review. **B is the number comparable to `PROC-02`, and it is the
headline below.** A is reported beside it because it is what this sweep originally published.

Both instants are read from the API as UTC ISO-8601 and compared as UTC; no local-offset
arithmetic is used anywhere, because subtracting local from UTC has produced wrong elapsed times
in this repository before.

**The patterns, published verbatim** so that every count below reproduces exactly. All are Python
`re` patterns applied case-insensitively (`re.I`) to the comment body as returned by the API; a
pattern matches when `search()` finds it anywhere in the body.

```text
P1  review\s+record

HB  (reviewed\s+head|head\s+reviewed|bind(?:s|ing)?\s+to\s+head|bound\s+to\s+head)

V   \b(SHIP-WITH-NITS|SHIP|ACCEPT|APPROVE|APPROVED|REVISE|FIX-FIRST|FIX FIRST|REJECT)\b
    |\bno objection to merging\b
    |\bapprove-with-nits\b

P4  <!--\s*codex-pull-request-review-summary\s*-->

U   P1 OR (HB AND V)              <-- the reported union

MARKER  (a merge receipt self-identifies with any one of these three phrases)
    MERGE\s+RECEIPT
    Disposition:\s*MERGED
    STAGE\s+G
```

The verdict-token set **V** is exactly the one used, with no implicit additions: the four register
verdicts `SHIP`, `ACCEPT`, `REVISE`, `FIX-FIRST`; the two spellings `SHIP-WITH-NITS` and
`FIX FIRST` that the records actually use; the review verbs `APPROVE`, `APPROVED` and `REJECT`;
and the two phrases `no objection to merging` and `approve-with-nits`. **`ABSTAIN` is deliberately
absent** — the schema records it as a judge outcome, never an expected label or a reviewer verdict;
and bare `NITS` is absent because it never appears without `SHIP-WITH-NITS`.

**A warning for anyone re-running the register's detector: its sentence has two clauses, and they
do not agree.** The first is *"whose body contains a verdict"* — read literally on its own that is
the `V` pattern, and measured it returns **32** pull requests. The second is *"the earliest
review-record timestamp"* — the record pattern, `U` — and measured it returns **15**, the figure
reported here. **This append adopts the second**, because *"record"* is the term the sentence is
defining and because `U` is the pattern this sweep publishes; the narrower `P1` reading gives
**8**. The 17-pull-request spread between the two clauses is why the definition is stated rather
than assumed — **a re-runner who takes the first clause literally will get a different headline**, 
and should cite that clause rather than this append's figure.

| id | pattern (as published above) | comments matched | merged PRs with ≥1 match | merged PRs with **zero** match |
| --- | --- | --- | --- | --- |
| **P1** | `review\s+record` | 90 | 59 | 582 |
| **P2** | `HB` **and** `V` | 201 | 114 | 527 |
| **P3** | `V` alone — loose upper bound, **not** the finding | 430 | 242 | 399 |
| **P4** | the Codex bot marker — a *different* reviewer family, for contrast | 169 | 163 | 478 |
| **U** | **U = P1 ∨ P2** | 244 | 141 | 500 |

Every row splits the same **641** merged pull requests: `≥1 + zero = 641` in each case
(59+582, 114+527, 141+500, …), which is the arithmetic check that the match
set is a subset of the enumerated population. **The zero-match figure is `500`**, computed as
`641 − 141` under the union U defined above. An earlier draft printed **496** in the table and
**500** in the prose, because the table's row had been computed with one extra head-binding
alternative — `bound head` and `head bound` — that the union did not include. That variant is real
and is worth recording, but it is not part of U:

- adding `bound head` and `head bound` to `HB` gives **145** any-match PRs and **496** zero,
  with the **same findings** — the finding set is insensitive to the choice, while the any-match
  count is not, which is exactly why the pattern had to be published rather than assumed.

**The inline-diff endpoint contributed 0 findings**, and the reason is a **pattern** result rather
than a timing result. Its 879 rows are the Codex bot's inline review comments and the author's
replies — a different artifact class from this repository's review records — and **191 of them do post
after their pull request's `mergedAt`** (all 191 by `chatgpt-codex-connector[bot]`; the first is PR #29, created
`2026-07-07T21:51:27Z` against a merge at `21:51:23Z`). **None of those
191 matches P1, and none matches P2, so none is a review record.** An earlier draft said that no
inline row was a post-`mergedAt` record; that clause was false by 191 rows. The conclusion was right
and the reason was wrong, and the reason is corrected here rather than deleted.

**Counting methods, named as `PROC-04` requires.** Every count in this append is an exact count of
matching records: pull-request counts and row counts are the length of a set or a list; percentages
are that count over the stated denominator (641 merged pull requests at this measurement). No line count
is published in this append; where one appears elsewhere in this page it is a **newline count** —
the number of `0x0A` bytes — and `Measure-Object -Line` is not used, because it drops blank lines.

### Findings — 15 merged pull requests under the register's own detector, 27 under the per-comment rule

**The reported figure is `15`.** It is the register's own after-the-fact detector (definition B above):
the pull request's **earliest** record-matching comment postdates its merge. The per-comment rule
gives **27**, which is what this sweep originally published, and the 12-pull-request difference is
itemised below rather than left as a discrepancy.

`class` is taken from each record's **own words**, not inferred from timing: **A** the record says the
review itself happened *before* the merge and only the posting was late; **B** the record says the
review was performed *after* the merge; **C** the record says the merge landed while the review was
running; **D** the record states the PR was already merged when written; **E** the record is a
correction or retraction of another record, not a review of the change; **F** the record carries no
provenance statement, recorded as *unsure* rather than guessed.

| PR | mergedAt (UTC) | earliest matching record (UTC) | lag (min) | class |
| --- | --- | --- | --- | --- |
| #557 | `2026-09-30T02:52:05Z` | `2026-09-30T04:34:14Z` | 102.15 | A |
| #555 | `2026-09-30T03:08:06Z` | `2026-09-30T04:34:12Z` | 86.10 | A |
| #558 | `2026-09-30T03:14:33Z` | `2026-09-30T04:34:15Z` | 79.70 | A |
| #559 | `2026-09-30T03:14:51Z` | `2026-09-30T04:34:16Z` | 79.42 | A |
| #560 | `2026-09-30T03:54:41Z` | `2026-09-30T04:34:17Z` | 39.60 | A |
| #562 | `2026-09-30T05:31:27Z` | `2026-09-30T05:31:48Z` | 0.35 | A |
| #563 | `2026-09-30T08:31:36Z` | `2026-09-30T08:36:08Z` | 4.53 | A |
| #568 | `2026-09-30T18:04:56Z` | `2026-10-02T23:47:54Z` | 3222.97 | B |
| #578 | `2026-09-30T23:20:19Z` | `2026-09-30T23:20:41Z` | 0.37 | A |
| #595 | `2026-10-01T17:36:53Z` | `2026-10-02T23:52:18Z` | 1815.42 | E |
| #597 | `2026-10-02T02:23:16Z` | `2026-10-02T23:49:04Z` | 1285.80 | B |
| #602 | `2026-10-02T02:32:16Z` | `2026-10-02T23:49:28Z` | 1277.20 | B |
| #611 | `2026-10-02T03:54:57Z` | `2026-10-02T04:10:14Z` | 15.28 | F |
| #626 | `2026-10-03T00:10:41Z` | `2026-10-03T00:11:52Z` | 1.18 | F |
| #627 | `2026-10-03T00:10:55Z` | `2026-10-03T00:13:11Z` | 2.27 | F |

**The `disposition` column has been removed rather than repaired.** An earlier draft carried a
`disposition recorded?` column whose `yes` meant only that the pull request number **appears** in
this register or in `.coord/coordinator-cadence.jsonl`. A membership test over mentions is not a
disposition of a late record — a PR number occurs in those files for unrelated reasons, including
as a row in an earlier merged-PR count series — so the column asserted more than its method
established. It is **withdrawn**, not renamed, because a renamed column would still invite the
reading it cannot support.

### The 12 pull requests the per-comment rule adds — and why the register's detector does not

| PR | receipt? | why the per-comment rule counts it and the register's detector does not |
| --- | --- | --- |
| #609 | no | an earlier record for the same pull request precedes the merge, so the merge gated a review |
| #613 | no | an earlier record for the same pull request precedes the merge, so the merge gated a review |
| #623 | no | an earlier record for the same pull request precedes the merge, so the merge gated a review |
| #625 | no | an earlier record for the same pull request precedes the merge, so the merge gated a review |
| #637 | no | an earlier record for the same pull request precedes the merge, so the merge gated a review |
| #648 | **yes** | a merge receipt, which postdates the merge by construction while the review record precedes it |
| #649 | **yes** | a merge receipt, which postdates the merge by construction while the review record precedes it |
| #650 | **yes** | a merge receipt, which postdates the merge by construction while the review record precedes it |
| #651 | **yes** | a merge receipt, which postdates the merge by construction while the review record precedes it |
| #652 | **yes** | a merge receipt, which postdates the merge by construction while the review record precedes it |
| #653 | **yes** | a merge receipt, which postdates the merge by construction while the review record precedes it |
| #656 | **yes** | a merge receipt, which postdates the merge by construction while the review record precedes it |

The seven receipts are recognised by the published `MARKER` pattern. **A merge receipt states the
head it merged and a disposition, so it satisfies `HB ∧ V` by construction** — that is a property of
what a receipt *is*, not of how the patterns are written, and tightening `P1`, `HB` or `V` to exclude
receipts would also exclude genuine records that quote the merge. **The register's own detector
excludes them structurally instead:** a receipt cannot be a pull request's *earliest* matching
comment when a review record for that same pull request precedes the merge, which is precisely what
a compliant merge looks like. **Under definition B, no receipt is a finding** — measured, the set of
B findings that match `MARKER` is empty.

### What the findings are, and what they are not

| subset | register's detector (B) — reported | per-comment rule (A) | A, receipts excluded |
| --- | --- | --- | --- |
| all findings (distinct PRs) | **15** | 27 | 20 |
| class **A** only — the review preceded the merge, so only the posting was late | 8 | 8 | 8 |
| class **E** — corrections or retractions, not reviews of the change | 1 | 2 | 2 |
| **governance-relevant (B, C, D or F), de-duplicated** | **6** | **17** | **10** |
| class **F** rows | 3 | 11 | 4 |

The class-A and class-E pull requests are **not** evidence that a merge escaped review. In class A
the review demonstrably preceded the merge and only the written record was late; in class E the
comment is not a review of the change at all. **The governance-relevant subset is therefore
6 pull requests under the register's detector**, and it is that number that should be compared against
the rule.

### Any-match and zero-match, corrected

An earlier draft published a receipt-excluded pair of `134` and `506`. **That was wrong by six, and
the corrected pair is `141` and `500` — the same as the unfiltered figures — for a reason worth
stating:** every receipt-bearing pull request **also** carries a non-receipt `U` match, and in every
case it is a record posted **before** the merge. Dropping the receipt **rows** therefore removes no
pull request from the any-match set. Measured, per receipt-bearing pull request:

| PR | `U` matches | non-receipt `U` matches | of those, posted before the merge |
| --- | --- | --- | --- |
| #648 | 3 | 2 | 2 |
| #649 | 3 | 2 | 2 |
| #650 | 2 | 1 | 1 |
| #651 | 3 | 2 | 2 |
| #652 | 2 | 1 | 1 |
| #653 | 10 | 3 | 3 |
| #656 | 3 | 2 | 2 |

**So the receipt contamination affects the findings count, not the denominator.** Excluding receipt
rows changes the findings from 27 to 20 and the class-F rows from 11 to 4; it does **not** move the
any-match population (**141**) or the zero-match population (**500**). An earlier draft subtracted whole
pull requests from the any-match set, which double-counted the correction and overstated the
zero-match gap by six.

### The larger half this sweep does not detect

The rule is *"do not merge before a review record bound to the current head is posted"*. This
sweep detects the case where a record was posted **late**. It structurally cannot detect the case
where **no record was ever posted**, because with no matching comment there is nothing to compare
against `merged_at`. That population is measured here as the zero-match column, and it is far
larger:

- **582 of 641 merged pull requests (90.8 %)** have no comment matching P1 at any time,
  before or after their merge;
- **527 (82.2 %)** under P2, the head-binding-and-verdict pattern;
- **500 (78.0 %)** under the reported union U.

**A merged pull request with no matching comment is not evidence that no review happened.** It
means no comment in this corpus matched the pattern. A review conducted in a session and never
posted leaves no retrievable trace at all, and the repository's own records say so — a no-change
reading *"leaves no artifact in the repository and is therefore NOT independently falsifiable"*.
The zero-match population is a **detection gap**, not a count of unreviewed merges, and closing it
needs a different instrument from this one.

### The machine-marker route to an exact receipt figure

A review pass identified the one route that would make receipt exclusion exact rather than
pattern-based: give merge receipts a **stable machine marker** — an invisible HTML comment, of
exactly the kind this append's own `P4` already matches, which discriminates because it is
machine-written rather than self-described. Receipts written after such a convention become
**deterministically excludable**. The same review reports that it tried the other candidate
discriminators and they failed: **author identity is unavailable** here (one account posts
everything), and a **merge-commit anchor** finds all the receipts but also several genuine review
rows. **This append does not adopt the convention** — it governs how future receipts are written,
which is broader than this artifact. It is recorded as the identified route, attributed to the
review that found it. **With definition B reported as the headline, the marker is no longer
load-bearing for the primary figure**, since the register's detector excludes receipts structurally.

### Recurrence — and a correction to the precedent this page cites

Item 2 above cites the cadence log entry `2026-10-01T20:22:51-07:00` — *"PRs #605 and #607 had
merged with `reviews=[]` … review never posted"* — as evidence that this is a recurrence.
**Re-measured, that precedent is half right, and the half that is wrong matters.** An earlier draft
of this append claimed *"the two commands' outputs are quoted rather than summarised"* and quoted
nothing; the actual records are below, and they are the evidence for the table that follows.

```text
$ gh api /repos/ModernNomad-98/Project-Aegis/pulls/605 \
    --jq '{merged_at, head: .head.sha, comments}'
#605  merged_at=2026-10-02T03:07:53Z  head=6b30b9d91f3c6f460e94d4a801777154dfaa6cb8  comments=5

$ gh api --paginate /repos/ModernNomad-98/Project-Aegis/issues/605/comments \
    --jq '.[] | {id, created_at, author: .user.login, first: (.body | split("\n")[0])}'
  5944665363  2026-10-02T02:47:31Z  chatgpt-codex-connector[bot]  You have reached your Codex usage limits …
  5944723882  2026-10-02T02:53:08Z  ModernNomad-98   ## CI evidence — exact head `9473ec64c5b8…`
  5944885937  2026-10-02T03:07:39Z  ModernNomad-98   ## Independent review record - AUDIT-3 (APPROVE WITH NITS)
  5944927849  2026-10-02T03:12:01Z  ModernNomad-98   ## ⚠️ Head change during review — `9473ec64` → `6b30b9d9`
  5945007480  2026-10-02T03:20:45Z  ModernNomad-98   ## Closeout — merged by the owner, not by this agent

$ gh api --paginate /repos/ModernNomad-98/Project-Aegis/issues/607/comments \
    --jq '.[] | {id, created_at, author: .user.login, first: (.body | split("\n")[0])}'
  5944850388  2026-10-02T03:04:02Z  chatgpt-codex-connector[bot]  You have reached your Codex usage limits …
#607  merged_at=2026-10-02T03:21:27Z  head=c629557f835343e4e39a024e3dfa5012cac06735  comments=1
```

**#605.** Comment **`5944885937`**, created **`2026-10-02T03:07:39Z`** — **fourteen seconds before**
the merge at `03:07:53Z` — opens `## Independent review record - AUDIT-3 (APPROVE WITH NITS)` and
contains the line *"the reviewed head `6b30b9d9` carries the fix"*, naming the head that merged.
**The cadence entry's "review never posted" clause is therefore FALSIFIED for #605.**

**#607.** One comment, **`5944850388`**, created `2026-10-02T03:04:02Z`, and it is the Codex
usage-limit notice — not a review record. **The clause holds for #607.**

So the **recurrence is real but the mechanism differs by PR**: #607 is a merge with *no* review
record at all, while #605 carried a record bound to the merged head posted fourteen seconds before
the merge. The cadence entry's `reviews=[]` was true in both cases and uninformative in both,
because formal review objects are empty on exactly these agent-authored pull requests — the same
narrow fact this append's method section states. **Neither PR is a finding of this sweep** — #605's
record precedes its merge, and #607 has no record to post — which is the clearest statement of what
this sweep does and does not detect.

**Where the correction is tracked — and one thing that is `unsure`.** The falsification above and
the evidence for it are tracked **in this append**. What is **not** tracked is anything that will
carry the correction *into* the cadence entry: that entry is append-not-edit, so the only way it
becomes true is a later cadence append by whoever maintains the log, and **no open issue,
owed-work item or register entry owns that.** Checked at this revision: the repository has **1**
open issue (#101), and it is not this; owed-work items 1–5 above name no such owner. **That
destination is therefore `unsure`.** The conflict's owner is named as `source-of-truth-reconciler`,
and owning a hand-off is not the same as owning a tracked destination; this append does not claim
one exists.

### The earlier sweep, labelled

The first row of the scope series — **20 of 634** — was produced in a prior agent session whose
intermediate inputs were not preserved. **It is recorded as UNVERIFIED.** It is not reproducible
from anything in this repository, its figures were computed with an earlier and looser pattern set,
and it should not be read as a confirmed earlier measurement or compared arithmetically with the
rows below it. It is carried only because dropping it would hide that a first sweep happened.

### How a reader re-runs the sweep

```text
# 1. merge-state enumeration and the completeness cross-check
$ gh pr list --state merged --limit 1000 --json number,title,mergedAt -R ModernNomad-98/Project-Aegis
$ gh pr list --state all    --limit 1000 --json number,state    -R ModernNomad-98/Project-Aegis
# 2. both comment corpora, in bulk
$ gh api --paginate --slurp "/repos/ModernNomad-98/Project-Aegis/issues/comments?per_page=100"
$ gh api --paginate --slurp "/repos/ModernNomad-98/Project-Aegis/pulls/comments?per_page=100"
# 3. join per PR and compare, both instants UTC:
#    definition A (per-comment) : ANY matching comment.created_at  >  pr.merged_at
#    definition B (this page)   : MIN matching comment.created_at  >  pr.merged_at   <- reported
#    classify with the published patterns: U = P1 OR (HB AND V)
```

Two properties make this reproducible in one pass. The join is keyed on the comment's own
`issue_url`, so no per-PR call is needed, and both instants are already UTC strings, so no timezone
conversion is involved. **`gh api` does not accept `-R`** — the owner and repository go in the
endpoint path — while `gh pr list` requires `-R` or a working directory inside a git repository. A
re-run at a later revision will return a **new** window, not a reproduction of this one; that is
why the scope is published as a series, and why the patterns above are published rather than
described.

### What this append does not claim

It does not rewrite, renumber or annotate owed-work items 1–5, or any class, rule or evidence row
above; item 2 is discharged here and left standing there. It does not claim the zero-match
population is unreviewed work. It does not claim any finding was a defect in the change that
merged — the sweep measures the **record's timing relative to the merge**, not the quality of the
merge or of the review, and it asserts no verdict about any pull request. It does not present
either definition as the only one: **A and B are both published, B is reported, and the difference
is itemised.** It does not correct the cadence log entry it quotes: the falsification of that
entry's #605 clause is recorded here, and the entry itself is left as written, because this
register's practice is to append a correction rather than edit a dated record. It adds no gate:
nothing in `scripts/` or `.github/` reads this table, and the sweep remains something an agent runs
rather than something a runner enforces.

**Provenance.** The sweep was run read-only against the GitHub API as `ModernNomad-98` on
2026-10-03, from a self-contained clone of `ModernNomad-98/Project-Aegis` at
`origin/main` = `a3a72fe5f2c9504f3c97fc312b9250db67d761d5`, the base revision this append is
committed on. The corpus closed at the newest comment, `2026-10-03T21:23:54Z`; every count above is at that
instant and is a series value, not a constant. No provider or model call was made, no evaluator
was run, and no dependency was installed. Every PR number, instant, comment id and hash in this
append comes from the API response or from `git`, not from prose.


---

## Appended 2026-10-03 (fifth append) — `Q5`: two published counting claims corrected

This append is **pure addition** except for the one declared in-cell narrowing
recorded under Claim 2. It corrects two counting claims on this page that
measurement falsified, renumbers nothing, rewrites no entry and adds no rule.

**Claim 1 — L2023–2024, corrected outright.** The page says:

> - **One class's central figure is unverified.** Class 5's "159 pages" figure is
>   not reproducible from `main`.

That sentence is **false**. The figure **is** obtainable from the default branch.
Method: a Python parse of the tracked
`tools/readability_acceptance/acceptance-index.json` (blob
`70c114c71be2e8c868347f9d14288e254ac81253`), counting the `reader_pages` rows
that carry no `last_acceptance_sha` and reading its `counts` block. Measured at
`origin/main` = `d9db0b83`: `counts.unknown` = **159**, `counts.recorded` =
**443**, `counts.reader_pages` = **602**, and **159 of the 602** `reader_pages`
rows carry no `last_acceptance_sha`, with 443 + 159 = 602. That tool's own
README names this population "no recorded acceptance", which is the quantity
Class 5's "159 pages have no review record" names at L603.

The correction also removes a contradiction **inside this page**: L2202 records
the figure as *"not re-derived by this pass; the instrument is now on `main` …
so re-derivation is possible"*, while L2023–2024 asserted it was not
reproducible.

**Two limits, carried with the correction and not resolved by assertion.**

1. **A fresh regeneration is UNVERIFIED (`unsure`).** The value above is
   reproduced from the tracked index, whose own `source_revision` is
   `d6e484189cc30c67dc69aeb973e15f89b693537d` and whose `counts.tracked_markdown`
   is **658**, against the **675** tracked Markdown files measured at
   `d9db0b83`. No run of `check_index.py` was made, so whether a fresh run still
   yields 159 at the current tree is not established.
2. **Set identity is UNPROVEN (`unsure`).** That the index's 159 rows are the
   *same* pages Class 5 counted is not established: the value and the definition
   agree; the membership does not.

**Claim 2 — L2070, narrowed in place, not deleted.** The `PROC-01` row of the
mechanically-enforceable table asserted that the machine-readable list it needs
"does not exist yet". A machine-readable, revision-keyed list **does** exist on
the default branch, and it landed **before** that sentence was written:
`tools/readability_acceptance/acceptance-index.json`, PR #629 at `1cb61f3a`
(2026-10-02T18:08:51-07:00), against this page's own PR #633 at `e88a0a0d`
(18:24:01). That row now carries the narrower true statement: what is still
absent is a list **declared for this gate** pairing each SHA with its **claim**
— the index pairs a SHA with its **page**. The original sentence is left
standing verbatim and the correction follows it in the same cell, the form the
`PROC-05` row of that same table already uses.

**What this append does not claim.** It does not re-derive or correct any other
figure on this page, and it does not annotate items 1–5 of the owed-work list.
It touches exactly one earlier line — the L2070 row named above — and that
narrowing is declared here rather than left silent. It adds no gate: the
`PROC-01` check remains unbuilt, and the mechanically-enforceable table's own
`scripts/` destination is unchanged. It does not resolve the two limits recorded
under Claim 1; it carries them.

---

## Appended 2026-10-03 (sixth append) — five operational findings from the merge gates, landed on owner decision

This append is **pure addition**. It rewrites no line above it, renumbers nothing, adds no stage and
changes no rule. It lands **five findings that were being carried in working memory, a chat message and
one untracked scratch file** — the class of carrier this register exists to replace.

**Authorisation.** Owner decision, 2026-10-03, on an audited recommendation, in the owner's words:
*"Register append, then decide AGENTS.md separately."* That decision authorises **this append only**.
**Nothing is written to `AGENTS.md` by this change**, and this append takes no position on what belongs
there — see *What this append does not claim*.

**Two of the five are new; three are instances of an existing rule.** `PROC-04`'s standing rule is at
**L539** of this page and its owed writing-standards half landed in the second append (**L2397**).
Findings **2**, **3** and **5** below are covered by it. They are recorded here as **instances with
evidence**, pointing at `PROC-04` rather than restating it, because a second rendering of a rule this
page already carries is itself the defect the policy forbids. Findings **1** and **4** are **not**
covered by any existing rule on this page.

**Each finding is marked with its kind.** A **look-up trap** is a query whose answer is misleading in a
way that produces a wrong action; a **record-keeping note** is about the fidelity of what gets recorded.
Both were hit **at a merge gate**, which is why they matter more than their size: a wrong reading there
produces a wrong action — a **false stop**, or a **false pass**.

| # | finding | kind | rule status |
| --- | --- | --- | --- |
| 1 | `commit_id` is re-anchored as a PR's diff moves; `original_commit_id` answers *"which head was this raised against"* | look-up trap | **new** |
| 2 | `gh api .../reviews` returns one page, and one page is not the count | look-up trap | `PROC-04` instance |
| 3 | `gh pr list --limit N` is a **cap**, not pagination, and a cap truncates silently | look-up trap | `PROC-04` instance |
| 4 | a job's `status` and its `conclusion` are different fields; the run-level state is authoritative | look-up trap | **new** |
| 5 | a verification that examined **nothing** reported success | record-keeping note | `PROC-04` instance — **relayed, not verified here** |

### 1. `commit_id` is re-anchored as a PR's diff moves — `original_commit_id` is the field that answers *which head*

**Kind: look-up trap. New — no existing rule on this page covers it.**

GitHub **re-anchors `commit_id`** on an inline review comment as the pull request's diff moves, so
`commit_id` answers *"which head does this comment attach to **now**"* — not *"which head was it raised
against"*. **`original_commit_id` is the stable field** and is the only one that answers the second
question.

**Evidence, PR #657**, six inline findings, read from
`gh api --paginate --slurp "/repos/ModernNomad-98/Project-Aegis/pulls/657/comments?per_page=100"`:

| field | value | findings carrying it |
| --- | --- | --- |
| `original_commit_id` | `9e5b79b97af5299f902c64c72b8f581407314dc7` | **all six** |
| `commit_id` | `9e5b79b97af5299f902c64c72b8f581407314dc7` | five, created `2026-10-03T18:38:46Z` |
| `commit_id` | `a3715be7a8d05ef20d5480a6fb33fc2cd5235a27` | **one — a P1**, id `4174408006`, created `2026-10-03T18:51:24Z` |

**The timestamps settle it, and they settle it the same way the field names do.** The two candidate
heads, dated from `git log -1 --format=%cI`:

- `9e5b79b9…` was committed `2026-10-03T11:25:21-07:00` — **`18:25:21Z`**;
- `a3715be7…` was committed `2026-10-03T14:26:28-07:00` — **`21:26:28Z`**.

The P1 was created at **`18:51:24Z`**, which is **two hours and thirty-five minutes before
`a3715be7…` existed**. It therefore **cannot** have been raised against `a3715be7…`. Its `commit_id`
was re-anchored to `a3715be7…` later, when that commit became the head; its `original_commit_id` still
names the head it was actually written against.

**Why this is a merge-gate finding and not trivia.** `a3715be7…` is the head that **merged** — PR #657
merged as `1e5961454f300261e195f5c71c4785fa723dc708` at `2026-10-03T21:39:30Z`. A merge agent reading
`commit_id` therefore sees a **P1 bound to the merged head**, which under this page's own entry
conditions is an untriaged P1 at the exact head being merged — an **automatic STOP**. The same agent
reading `original_commit_id` sees all six findings bound to the **previous** head, which is what
actually happened. **This nearly caused a false merge stop.** The reading is not ambiguous once the two
fields are told apart; the defect is that only one of them is named `commit_id`.

### 2. `gh api .../reviews` returns one page, and one page is not the count

**Kind: look-up trap. A `PROC-04` instance — see L539 and L2397.**

`GET /pulls/<n>/reviews` returns **GitHub's default page**, so a bare call reports whatever fits in one
page. **Measured:** `#77` reads **30** from a bare call — exactly the default page size — and **83**
with:

```text
$ gh api --paginate --slurp "/repos/ModernNomad-98/Project-Aegis/pulls/<n>/reviews?per_page=100"
```

**The neighbours were checked and none moved**, which is the part that makes the one instance
trustworthy: `#653` **7**, `#654` **2**, `#29` **1**, and **0** on `#650`, `#623`, `#611`, `#213` and
`#2`. Every one of those is **below the default page size**, so the cap could not have hidden anything
there. The single instance is a published count under a **truncated method** — which is the defect
`PROC-04` names and this append does not restate.

### 3. `gh pr list --limit N` is a cap, and a cap is not pagination

**Kind: look-up trap. A `PROC-04` instance — see L539 and L2397.**

`--limit N` **truncates silently when reached**; it does not page. A count from a capped call and a
count from a paginated one are **different claims**, and only the second is a count of the population.
**Measured:** `--limit 1000` returned **658**, and the API's own `Link: rel="last"` total for
`/pulls?state=all` was **658** — so the cap was **never reached** and the enumeration is complete.

The distinction is worth recording because the **outcome here was benign and the method was still
wrong**: the figure happened to be right, and nothing in the command said so. The check that makes it
right is the `Link` header, not the `--limit`.

### 4. A job's `status` and its `conclusion` are different fields; the run-level state is authoritative

**Kind: look-up trap. New — no existing rule on this page covers it.**

In the Actions API a job carries **both** a `status` and a `conclusion`, and they are not the same
quantity. **Measured on run `37156376468`**: the **run-level** state is `status: completed`,
`conclusion: success` — a finished, green run — while one of its jobs reports a **job-level
`status: in_progress` alongside a `conclusion: success`**:

| job | job `status` | job `conclusion` |
| --- | --- | --- |
| `gate-guard` | **`in_progress`** | **`success`** |
| `validate-skills` | `completed` | `success` |
| `windows-offline-checks` | `completed` | `success` |
| `tools-tests-linux` | `completed` | `success` |
| `tools-tests-windows` | `completed` | `success` |

**A reader who checks a job's `status` alone reads a finished, green run as unfinished** — and at a
merge gate that is a **false stop** produced by a correct query read through the wrong field.
**The run-level state is authoritative**, and when a job must be read, its `conclusion` is the field
that carries the outcome. This finding was **confirmed independently by the merge agent on #659** as
well as measured directly here.

### 5. A verification that examined nothing reported success

**Kind: record-keeping note, whose mechanism is a look-up defect. A `PROC-04` instance — see L539 and
L2397.**

**This one is relayed, and it is labelled relayed because it cannot be verified from here.** The
account comes from **`#654`'s merge agent**, relayed by the coordinator, and recorded in an
**untracked** scratch file —
`C:\temp\aegis-q5\Q5-SCOPE-CONFLICT-AND-MEASUREMENT-2026-10-03.md`, §13.2 — which is the carrier
that decays. In its own words:

> two of its three verification attempts returned the right answer for the wrong reason — a nested-array
> cast meant **zero comments were examined** while reporting success: *"Both would have let me report a
> pass that examined nothing — the exact failure class `PROC-02` exists to catch."*

**What was actually inspected here, and what was not.** This append's author read that account, quoted
it, and **did not** observe the agent's process, its scripts or its output, and **did not re-run its
verification**. It is therefore recorded as a **relayed account attributed to that agent**, not as a
verified fact about it. What *is* independently established is only what the account is an instance of:
a result can be reported as a pass while the set it was computed over is **empty**, and the artifact
the scratch file itself notes is that the empty set was invisible in the success it printed.

**It belongs on this page because it is the same shape as the rest of this register** — a reported
outcome that outran what was examined — and because its carrier was a file that no `grep` on this page
reaches. Landing it here is the whole point; verifying it is someone else's step, and this append says
so rather than implying otherwise.

### What this append does not claim

It does not restate `PROC-04`; findings **2**, **3** and **5** point at its standing rule at **L539**
and its landed writing-standards half at **L2397**, and this append is deliberately not a second
rendering of it. It does **not** claim finding **5** is verified — it is **relayed**, attributed to
`#654`'s merge agent, sourced from an untracked file, and the author did not re-run it; the
**relayed** label is load-bearing and should not be stripped by a later reader. It does not add
findings **1**, **2**, **3** or **4** to `AGENTS.md`, and it does not decide whether any of the five
belongs there: the owner's decision is *"Register append, then decide `AGENTS.md` separately"*, and
that second decision is untouched. It does not claim the five are the complete set of operational
traps at the merge gates — they are the five that were **being carried outside tracked artifacts**, which
is why they were the ones at risk. It changes no stage contract, adds no gate, and nothing in
`scripts/`, `.github/workflows/` or `tools/**` reads this section. It does not correct the two counts
recorded in the fourth and fifth appends above; those corrections stand as written.

**Provenance.** Every count and instant above other than finding 5's account was measured on
2026-10-03 against the GitHub API and a local clone at `origin/main` =
`3e992f896f7934d9e0f1043c75f942de715af520`; the PR and comment ids and the run id are quoted from the
API responses. Finding 5 is the single relayed item and is labelled as such in place. No provider or
model call was made, no evaluator was run, and no dependency was installed.
