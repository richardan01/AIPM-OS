# Proof of Work

AI Product Lab is an AI product engineering proof-of-work system. It shows how product judgment, agentic workflows, evals, quality gates, and failure logs can be composed into a measurable operating loop.

The portfolio claim is not "AI can write product documents." The stronger claim is: **AI-assisted product engineering can be designed, evaluated, governed, and improved with the same discipline expected from production systems.**

## What this proves

| Capability | Proof surface | What to inspect |
|---|---|---|
| AI product judgment | Problem framing, gates, kill criteria, and tradeoffs | `GOALS.md`, `Tasks/active.md`, `Agents/Gotham/thesis-q3-2026.md` |
| Agentic workflow architecture | Named agents, routing rules, handoffs, and human-in-the-loop pauses | `CLAUDE.md`, `Agents/`, `Workflows/` |
| Eval design | Offline suites, planted-flaw meta-evals, answer keys, and run protocols | `Evals/README.md`, `Evals/eval-audit-checklist.md` |
| Reliability discipline | CI replay, artifact gates, pending-rerun sentinels, and branch-protection config | `.github/workflows/quality-gates.yml`, `Tools/`, `scripts/` |
| Failure learning | Negative results, remediations, reruns, and open residuals | `Evals/run-log.md`, `Evals/failure-log.md` |
| Flagship measurable build | RegEval judge-alignment loop with κ scoring and contamination correction | `Evals/regeval/regeval-suite.md`, `Projects/ralph/brief.md` |

## Flagship measurable project: RegEval

RegEval is the flagship measurable project in this lab. It tests whether an LLM-as-judge workflow can classify regulated-domain compliance examples with enough agreement against human labels to be useful.

The point is not only the score. The point is the measurement loop:

- define a falsifiable metric;
- run the judge against a fixed dataset;
- compare against human labels;
- log failures and remediations;
- rerun with documented changes;
- preserve the run history so learning is visible over time.

This matters because regulated-domain AI products fail in ways that are easy to hide behind impressive demos. RegEval makes those failures measurable before the system is trusted.

## Latest public evidence snapshot

| Area | Latest public status | Evidence | Caveat |
|---|---|---|---|
| CI quality gates | Passing on `main` as of 2026-07-06 | [latest GitHub Actions run](https://github.com/richardan01/AI-Product-Lab/actions/runs/28797849060) | Branch protection still has to be applied in GitHub settings. |
| Onboarding workflow eval | Content pass on 2026-06-23; temporal evals pass on 2026-07-05 | `Evals/run-log.md` | Full transcripts/results are local and gitignored, so public auditability is summary-level. |
| Gate-group eval | First full run: r1 failed 6/8, remediation applied, r2 passed 7/8 on 2026-07-06 | `Evals/run-log.md`, `Evals/failure-log.md` | Ducard has a non-blocking schema residual: prose before JSON. |
| RegEval | κ-scored judge-alignment loop with logged corrections and contamination handling | `Evals/regeval/regeval-suite.md` | Reviewer should read caveats before treating any single score as final validation. |

## Quality gates protect public artifacts

Public artifacts are gated before they are treated as portfolio evidence. The quality-gate system is designed to catch:

- unsupported claims;
- unclear positioning;
- missing evidence;
- brittle methodology;
- reader confusion;
- overclaiming from partial eval results.

In this repo, those gates are part of the proof: they show how public-facing work is reviewed before it is shipped. Local hooks block gated writes, CI replays the checks, and artifact sidecars preserve the review trail.

## Evals and run logs show learning over time

The eval suites and run logs are the longitudinal evidence layer. They make the work inspectable by showing:

- what was measured;
- what failed;
- what changed;
- what improved;
- what remains uncertain.

That is the core portfolio claim AI Product Lab is meant to support: AI product engineering should become measurable proof-of-work rather than private notes, one-off prompts, or vague positioning.
