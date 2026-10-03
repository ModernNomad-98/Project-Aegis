# Code fixture with wrapped links

Every link below is documentation, so none may be resolved. A checker that
resolves code blocks reports broken links in documents that have none.

```markdown
[missing fenced target](nowhere.md)
[dead fenced anchor](#no-such-section)
[fenced wrapped
target](nowhere.md)
```

An inline mention: `[missing inline target](nowhere.md)`.

Real link, for contrast: [the good fixture](../good/README.md).
