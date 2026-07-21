# Public evidence — agent-harness

Raw traces (`evals/agent-harness/_traces/`) are gitignored: they are unsanitized session
records that may contain private paths, names, or content. This directory is the **opposite**
— a small set of **sanitized, end-to-end runs that ship publicly**, so the repo's grounding
claim is backed by visible proof instead of a private log.

## What goes here

- One or two fully worked runs: the normalized trace (redacted), the seven per-eval verdicts,
  and the aggregate — enough for a reader to see the method actually ran on a real session.
- One worked **failure → N-1 fixture → fix** story, when one exists. That narrative is the
  point of the whole lab.

## Sanitization checklist (before adding anything here)

- [ ] Replace absolute paths, usernames, org names, and any credential-shaped strings.
- [ ] Drop `params`/`result` bodies that carry private content; keep tool *names*, ok flags,
      and metrics (that is what the axes grade).
- [ ] Keep `goal` only if it is safe to publish; otherwise paraphrase it.
- [ ] Re-read the whole file before committing — sanitization is manual and easy to get wrong.

## Status

The directory contains a synthetic tutorial and one controlled real Codex tool-use run against
a public toy task. The controlled trace was reviewed across the same seven criteria; it is not
evidence that Codex can execute the shipped Claude Code orchestration command. Neither run is
production evidence or supports a population-level reliability claim.
