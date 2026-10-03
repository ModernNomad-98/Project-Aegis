# Good fixture

Valid relative file target: [the subdirectory readme](subdir/README.md).
Valid directory target: [the subdirectory](subdir/).
Valid directory target: [the skills directory](../../../../../.claude/skills/).
Valid in-page anchor: [see the details](#details).
Valid second anchor: [back to the top](#top).
External, never fetched: [the project](https://example.invalid/project).
External scheme, never fetched: [mail us](mailto:fixture@example.invalid).

<a id="explicit-anchor"></a>

Valid explicit HTML anchor: [defined by hand](#explicit-anchor).

## Details

Body text for the `details` anchor.

```text
This fenced block mentions a link that must NOT be resolved: [missing](nowhere.md)
```

Inline code mentioning `[also missing](nowhere.md)` must not be resolved either.
