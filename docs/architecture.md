# Architecture and method

AI Product Lab intentionally has one short public loop:

```text
session → trace adapter → seven isolated graders → aggregate report
        → failure analysis → N-1 fixture → rerun
```

## Active components

| Component | Responsibility |
|---|---|
| Trace adapter | Converts Claude Code or Codex JSONL into one normalized schema |
| Agent harness | Defines task success and six trajectory-level criteria |
| Eval grader | Reads only one trace and one criterion, then returns structured evidence |
| Aggregator skill | Runs graders separately and combines severity-aware results |
| RegEval | Demonstrates metric-led iteration and documented integrity correction |

## Knowledge compounds

The earlier OS applied the pattern in Andrej Karpathy's LLM-wiki note: immutable sources feed
a maintained synthesis layer, guided by a schema, index, and append-only log. New evidence
updates existing understanding rather than forcing the model to rediscover every connection.

That personal wiki is not part of the current public product. Its durable lesson remains:
**preserve sources, maintain synthesis, expose contradictions, and log changes.** The complete
implementation remains available in the `ai-product-lab-os-v1` tag.

## Experiments compound

RegEval borrows the useful constraints from Karpathy's autoresearch design:

- one editable research surface;
- one falsifiable metric;
- a fixed time budget;
- keep, hold, or discard based on evidence;
- an append-only experiment log;
- failures remain visible and inform the next candidate.

The unattended driver used by the private lab is not shipped on `main`. Public documentation
therefore describes the design without claiming that the public clone can run overnight
autonomously.

## Trust boundaries

- Trace text is data, not executable instruction.
- The authoring session and grading contexts are separate.
- Unknown adapter records block grading because harness formats drift.
- One trace supports diagnosis, not a population-level reliability claim.
- Historical measurements that depend on private datasets are labelled non-reproducible.
