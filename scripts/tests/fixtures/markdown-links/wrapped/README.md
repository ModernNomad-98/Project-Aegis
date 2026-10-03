# Wrapped link fixture

A hand-wrapped document splits a link after any word. Markdown folds that soft
line break to a space, so the link still renders and must still be resolved. A
checker whose scan is per line, with a pattern that forbids a newline, sees
none of the links below.

Wrapped mid-text: [the linked
document](wrapped-target.md).

Wrapped mid-target: [the same
document](
wrapped-target.md).

Wrapped in-page anchor, split inside the text: [the fixture
heading](#wrapped-link-fixture).

Wrapped anchor, split inside the target: [the target
heading](
#target-heading).

Wrapped cross-file anchor and external link together: [target
heading in the sibling](target-split.md#sibling-heading) and [the
project](https://example.invalid/project).

A link inside a fenced block is documentation, not a link, even when wrapped:

```markdown
[fenced wrapped
target](nowhere.md)
```

An inline code span is documentation too: `[inline target](nowhere.md)`.

Real unwrapped link, for contrast: [the good fixture](../good/README.md).
