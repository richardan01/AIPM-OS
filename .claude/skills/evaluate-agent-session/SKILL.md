---
name: evaluate-agent-session
description: Normalize and grade one Claude Code or Codex session with seven isolated graders.
argument-hint: "sample | <session-path> --harness claude-code|codex"
disable-model-invocation: true
---

# Evaluate an agent session

This is the only public workflow in AI Product Lab. `$ARGUMENTS` is either `sample` or an
absolute session path plus `--harness claude-code|codex`.

## 1. Resolve and disclose

For `sample`, use `evals/agent-harness/samples/coding-retry.json`. It is already normalized,
synthetic, and safe to grade; do not ask for privacy confirmation.

For any other input:

1. Parse exactly one path and one supported harness.
2. Show the resolved absolute path.
3. Display: “The selected trace may contain private code, paths, names, or credentials. Its
   content will be processed by your configured inference provider. Raw traces and reports
   stay gitignored unless you deliberately publish a sanitized copy.”
4. Ask: “Grade this trace? Reply exactly `yes, grade this trace` to continue.”
5. Stop unless the reply matches exactly.
6. Run:

   ```bash
   python3 scripts/preflight_agent_eval.py <path> --harness <harness> --confirm-private
   ```

Read the JSON output and use its `trace_path`. If preflight refuses the trace, report the
specific reason and stop.

For `sample`, run `python3 scripts/preflight_agent_eval.py sample` and use its `trace_path`.

## 2. Grade in isolation

Launch seven `eval-grader` subagents in parallel. Each receives only:

- `trace_path` from preflight;
- one matching criteria path under `evals/agent-harness/00-*` through `06-*`.

Do not grade in the parent context. Do not let any grader read another criterion or result.

## 3. Aggregate

Create a report object matching `evals/agent-harness/report-schema.json`:

- one axis row per grader, ordered `00` through `06`;
- `task_success` equals the `00` verdict;
- `bad_count` and `sad_count` count non-pass axis findings by severity;
- `overall_verdict` is `pass` only when task success passes and `bad_count` is zero;
- use `insufficient-evidence` when task success cannot be graded;
- recommend an N-1 fixture when a first upstream tool error or blocking trajectory failure
  exists; otherwise recommend grading more representative traces.

For private runs, write JSON and Markdown reports under
`evals/agent-harness/results/<trace-id>/`. For `sample`, display the report but do not write a
new committed artifact.

Validate any written JSON with:

```bash
python3 scripts/validate_agent_report.py <report.json>
```

## 4. Present

Lead with the overall verdict and task-success result. Then show a seven-row table with axis,
verdict, severity, and evidence. End with the recommendation and the report path, if written.

Never claim that one trace proves a reliability rate. Never publish or sanitize automatically.
