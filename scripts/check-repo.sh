#!/usr/bin/env bash
set -euo pipefail

required_files=(
  "README.md"
  "LICENSE"
  "CHANGELOG.md"
  "CLAUDE.md"
  "docs/learn.md"
  "docs/architecture.md"
  "docs/privacy.md"
  "docs/case-studies/gotham.md"
  ".claude/skills/evaluate-agent-session/SKILL.md"
  ".claude/agents/eval-grader.md"
  "evals/agent-harness/report-schema.json"
  "evals/agent-harness/evidence/controlled-real-run/report.json"
  "evals/regeval/demo/gold.jsonl"
  "evals/regeval/demo/predictions.jsonl"
)

for file in "${required_files[@]}"; do
  [[ -f "$file" ]] || { echo "Missing required file: $file" >&2; exit 1; }
done

allowed_roots='^(docs|evals|scripts|README\.md|LICENSE|CHANGELOG\.md|CLAUDE\.md)$'
for entry in $(git ls-files | cut -d/ -f1 | sort -u); do
  [[ "$entry" == .* ]] && continue
  [[ "$entry" =~ $allowed_roots ]] || { echo "Unexpected visible root entry: $entry" >&2; exit 1; }
done

removed_roots='^(Agents|Artifacts|Knowledge|Projects|Tasks|Templates|Tools|Workflows|_Registry|Evals)/'
if git ls-files | rg "$removed_roots"; then
  echo "Legacy OS surface is still tracked on main." >&2
  exit 1
fi

public_files=(README.md CLAUDE.md docs evals/README.md evals/agent-harness/README.md evals/regeval/README.md)
if rg -n -i '\b(tomorrow|today|this sprint|next sprint)\b' "${public_files[@]}"; then
  echo "Stale relative-date language found on the public path." >&2
  exit 1
fi

legacy_refs='(Evals/|Agents/|Artifacts/|Knowledge/|Projects/|Tasks/|Templates/|Tools/|Workflows/|_Registry/)'
if rg -n "$legacy_refs" "${public_files[@]}"; then
  echo "Reference to a removed path found on the public path." >&2
  exit 1
fi

tracked_count="$(git ls-files | wc -l | tr -d ' ')"
[[ "$tracked_count" -lt 220 ]] || { echo "Tracked surface is too large: $tracked_count files" >&2; exit 1; }

rg -q '^evals/\*/_traces/$' .gitignore
rg -q '^evals/\*/results/$' .gitignore

echo "Repository contract passed ($tracked_count tracked files)."
