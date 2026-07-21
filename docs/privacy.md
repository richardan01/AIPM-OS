# Privacy model

Agent sessions may contain source code, local paths, names, customer information, credentials,
or text copied from private systems. Treat every raw trace as sensitive by default.

## What stays local

- Normalized traces are written under `evals/*/_traces/`, which is gitignored.
- Generated private reports are written under `evals/*/results/`, which is gitignored.
- No hosted tracing or observability service is required.

## What leaves the machine

When Claude Code grades a trace, the selected trace content and criterion are processed by
the user's configured inference provider. “Local files” does not mean “no inference egress.”

The evaluator must show this disclosure and obtain explicit confirmation before grading any
non-sample trace.

## Before publishing evidence

1. Replace absolute paths, usernames, organization names, and credentials.
2. Remove tool parameters or results containing private content.
3. Retain only the evidence needed to understand the verdict.
4. Re-read the complete artifact manually.
5. Label whether the run is synthetic, controlled real, or production-derived.

Never move a raw trace directly from `_traces/` into the public evidence directory.
