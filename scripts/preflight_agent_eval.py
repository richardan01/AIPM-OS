#!/usr/bin/env python3
"""Resolve, normalize, and validate an agent trace before LLM grading."""

import argparse
import json
import sys
from pathlib import Path

import trace_adapter

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "evals" / "agent-harness" / "samples" / "coding-retry.json"


def fail(message):
    print(json.dumps({"status": "blocked", "reason": message}))
    raise SystemExit(2)


def validate(trace):
    if not isinstance(trace, dict):
        fail("trace root must be a JSON object")
    if not trace.get("goal"):
        fail("trace goal is null or empty")
    if not isinstance(trace.get("turns"), list) or not trace["turns"]:
        fail("trace has no conversation turns")
    if not isinstance(trace.get("tool_calls"), list) or not trace["tool_calls"]:
        fail("trace has no tool calls; trajectory axes cannot be graded")
    skipped = trace.get("skipped_lines") or {}
    known_noncontent_records = {"unknown", "session_meta", "session", "config", "meta", "sidechain"}
    unknown_skips = skipped.get("unknown", 0) + sum(
        count for kind, count in skipped.items()
        if kind not in known_noncontent_records and isinstance(count, int)
    )
    if unknown_skips != 0:
        fail("trace contains unknown skipped records; update the adapter before grading")
    if not trace.get("final_output"):
        fail("trace has no final output")


def validate_jsonl_syntax(path):
    with path.open(encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, start=1):
            if not raw.strip():
                continue
            try:
                json.loads(raw)
            except json.JSONDecodeError as exc:
                fail(f"could not normalize session: malformed JSON record at line {line_number}: {exc.msg}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="sample or a session JSONL path")
    parser.add_argument("--harness", choices=["claude-code", "codex"])
    parser.add_argument("--confirm-private", action="store_true")
    parser.add_argument("--out", help="explicit normalized trace output path")
    args = parser.parse_args()

    if args.source == "sample":
        trace_path = SAMPLE
        trace = json.loads(trace_path.read_text(encoding="utf-8"))
        run_kind = "synthetic"
    else:
        if not args.harness:
            fail("--harness is required for a session path")
        if not args.confirm_private:
            fail("privacy confirmation is required for a non-sample trace")
        source = Path(args.source).expanduser().resolve()
        if not source.is_file():
            fail(f"session file does not exist: {source}")
        validate_jsonl_syntax(source)
        try:
            trace, session_id = (
                trace_adapter.adapt_claude_code(source)
                if args.harness == "claude-code"
                else trace_adapter.adapt_codex(source)
            )
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            fail(f"could not normalize session: {exc}")
        trace["session_id"] = session_id
        trace["trace_id"] = trace_adapter._next_trace_id("agent-harness")
        trace_path = Path(args.out).expanduser().resolve() if args.out else (
            ROOT / "evals" / "agent-harness" / "_traces" / "files" /
            f"{trace['trace_id']}.json"
        )
        run_kind = "private"

    validate(trace)
    if args.source != "sample":
        trace_path.parent.mkdir(parents=True, exist_ok=True)
        trace_path.write_text(json.dumps(trace, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps({
        "status": "ready",
        "run_kind": run_kind,
        "trace_id": trace["trace_id"],
        "source_harness": trace["source_harness"],
        "trace_path": str(trace_path),
        "turn_count": len(trace["turns"]),
        "tool_call_count": len(trace["tool_calls"]),
    }))


if __name__ == "__main__":
    main()
