## What and why

<!-- Explain the user-facing change and why it belongs in this proof-of-work lab. -->

## First-timer impact

<!-- Can a visitor understand and try the evaluator more easily? -->

## Validation

- [ ] `bash scripts/check-repo.sh`
- [ ] `python3 scripts/test_trace_adapter.py`
- [ ] `python3 scripts/test_eval_entrypoint.py`
- [ ] `python3 scripts/check_markdown_links.py`
- [ ] `npx --yes markdownlint-cli@0.39.0 "**/*.md" --ignore node_modules`

## Privacy and evidence

- [ ] No raw private trace, provider secret, personal path, or unsanitized report is tracked.
- [ ] Evidence is labelled synthetic, controlled real, or production accurately.
- [ ] Claims identify what is and is not reproducible from the public clone.
