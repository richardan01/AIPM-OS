# Agent harness

Agent harness grades a real Claude Code or Codex session in two phases: final task success
and six trajectory-level diagnostics.

## Fastest path

Start Claude Code at the repository root and run:

```text
/evaluate-agent-session sample
```

For a completed private session:

```text
/evaluate-agent-session /absolute/path/to/session.jsonl --harness claude-code
/evaluate-agent-session /absolute/path/to/rollout.jsonl --harness codex
```

The command performs privacy confirmation, normalization, validation, seven isolated grades,
aggregation, and local report validation.

## What it returns

- one task-success verdict;
- six trajectory-axis verdicts;
- evidence for every finding;
- `bad` and `sad` severity counts;
- an overall verdict and recommended next action.

A trace passes only when task success passes and no axis has a `bad` finding. One trace is a
diagnostic data point; grade a representative set before reporting a rate.

## Files

| Path | Purpose |
|---|---|
| `00-*` through `06-*` | One binary criterion set per isolated grader |
| `samples/` | Synthetic trace and adapter regression fixtures |
| `evidence/` | Sanitized tutorial and controlled-real public reports |
| `protocol.md` | Manual and advanced run procedure |
| `agent-harness-suite.md` | Methodology and scoring rationale |
| `../_schema/trace-schema.md` | Normalized trace contract |
| `report-schema.json` | Aggregate report contract |

## Support status

| Surface | Status |
|---|---|
| Claude Code input | Verified against a real session |
| Codex input | Regression-tested against the committed sample format |
| Claude Code grading | Active runner |
| Codex grading runner | Not shipped |
| Cowork | Planned; format unconfirmed |

Raw `_traces/` and private `results/` are gitignored. Read
[`docs/privacy.md`](../../docs/privacy.md) before grading work sessions.
