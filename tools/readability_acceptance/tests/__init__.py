"""Regression tests for the readability-acceptance tool, importable as a package.

This file makes the modules here importable as
`tools.readability_acceptance.tests.*` when `python -m unittest discover -s
tools/readability_acceptance/tests` runs with the checkout root on `sys.path`
(the `-m` invocation the `tools-tests` jobs already use), instead of being
loaded as top-level modules. The sibling test packages under `tools/` follow
the same `-m unittest discover` pattern.
"""
