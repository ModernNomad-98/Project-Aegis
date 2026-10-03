# Wrapped link fixture

The unwrapped twin of `README.md` in this directory: exactly the same links,
each written on one line, with the same targets and the same anchors. A
checker that resolves wrapped links must report identical counts for both
files, and this one is the control -- its counts are the numbers `README.md`
has to match, so neither file can drift without the comparison failing.

Wrapped mid-text: [the linked document](wrapped-target.md).

Wrapped mid-target: [the same document](wrapped-target.md).

Wrapped over three lines, ending in a cross-file anchor: [the target heading in the wrapped target](wrapped-target.md#target-heading).

Wrapped in-page anchor, split inside the text: [the fixture heading](#wrapped-link-fixture).

Wrapped cross-file anchor: [target heading in the sibling](target-split.md#sibling-heading).

The next source line holds a complete link AND the start of a wrapped one, so
the join must not be refused merely because the line already parses:
[the earlier target](wrapped-target.md) and [the cross-file anchor](target-split.md#sibling-heading).

External link, wrapped: [the project](https://example.invalid/project).

Real unwrapped link, for contrast: [the good fixture](../good/README.md).
