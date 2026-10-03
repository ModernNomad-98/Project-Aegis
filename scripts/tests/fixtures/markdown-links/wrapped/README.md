# Wrapped link fixture

A hand-wrapped document splits a link after any word. Markdown folds that soft
line break to a space, so the link still renders and must still be resolved. A
checker whose scan is per line, with a pattern that forbids a newline, sees
none of the wrapped links below, so this file is checked against its unwrapped
twin (`unwrapped-twin.md`), which carries the same links on one line each and
must produce the same counts.

Wrapped mid-text: [the linked
document](wrapped-target.md).

Wrapped mid-target: [the same document](
wrapped-target.md).

Wrapped over three lines, ending in a cross-file anchor: [the target
heading in the wrapped
target](wrapped-target.md#target-heading).

Wrapped in-page anchor, split inside the text: [the fixture
heading](#wrapped-link-fixture).

Wrapped cross-file anchor: [target
heading in the sibling](target-split.md#sibling-heading).

The next source line holds a complete link AND the start of a wrapped one, so
the join must not be refused merely because the line already parses:
[the earlier target](wrapped-target.md) and [the cross-file
anchor](target-split.md#sibling-heading).

External link, wrapped: [the
project](https://example.invalid/project).

A link inside a fenced block is documentation, not a link, even when wrapped:

```markdown
[fenced wrapped
target](nowhere.md)
```

An inline code span is documentation too: `[inline target](nowhere.md)`.

A code span that wraps is one code span, and still documentation: `[a wrapped
code span](nowhere.md)`.

Real unwrapped link, for contrast: [the good fixture](../good/README.md).
