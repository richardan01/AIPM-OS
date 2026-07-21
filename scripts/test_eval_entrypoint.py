#!/usr/bin/env python3
"""Regression tests for evaluator preflight and report validation."""

import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT = ROOT / "scripts" / "preflight_agent_eval.py"
VALIDATE = ROOT / "scripts" / "validate_agent_report.py"
CODEX_SAMPLE = ROOT / "evals" / "agent-harness" / "samples" / "codex-rollout-sample.jsonl"
PUBLIC_REPORT = ROOT / "evals" / "agent-harness" / "evidence" / "controlled-real-run" / "report.json"


def run(*args, ok=True):
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    if ok and result.returncode != 0:
        raise AssertionError(result.stdout + result.stderr)
    if not ok and result.returncode == 0:
        raise AssertionError("expected failure: " + " ".join(map(str, args)))
    return result


def write_jsonl(path, rows):
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")


def main():
    sample = run("python3", str(PREFLIGHT), "sample")
    assert json.loads(sample.stdout)["status"] == "ready"

    with tempfile.TemporaryDirectory() as raw_tmp:
        tmp = Path(raw_tmp)
        out = tmp / "codex.json"
        result = run("python3", str(PREFLIGHT), str(CODEX_SAMPLE), "--harness", "codex",
                     "--confirm-private", "--out", str(out))
        assert json.loads(result.stdout)["source_harness"] == "codex"
        assert out.exists()

        blocked = run("python3", str(PREFLIGHT), str(CODEX_SAMPLE), "--harness", "codex", ok=False)
        assert "privacy confirmation" in blocked.stdout

        malformed = tmp / "malformed.jsonl"
        malformed.write_text("{not-json}\n", encoding="utf-8")
        result = run("python3", str(PREFLIGHT), str(malformed), "--harness", "codex",
                     "--confirm-private", ok=False)
        assert "could not normalize" in result.stdout

        null_goal = tmp / "null-goal.jsonl"
        write_jsonl(null_goal, [
            {"type": "session_meta", "payload": {"id": "null"}},
            {"type": "response_item", "payload": {"type": "function_call", "name": "shell", "arguments": "{\"command\":\"ls\"}", "call_id": "c1"}},
            {"type": "response_item", "payload": {"type": "function_call_output", "call_id": "c1", "output": "file.txt"}},
            {"type": "response_item", "payload": {"type": "message", "role": "assistant", "content": "done"}},
        ])
        result = run("python3", str(PREFLIGHT), str(null_goal), "--harness", "codex",
                     "--confirm-private", ok=False)
        assert "goal is null" in result.stdout

        empty_tools = tmp / "empty-tools.jsonl"
        write_jsonl(empty_tools, [
            {"type": "session_meta", "payload": {"id": "empty"}},
            {"type": "response_item", "payload": {"type": "message", "role": "user", "content": "Say hello"}},
            {"type": "response_item", "payload": {"type": "message", "role": "assistant", "content": "hello"}},
        ])
        result = run("python3", str(PREFLIGHT), str(empty_tools), "--harness", "codex",
                     "--confirm-private", ok=False)
        assert "no tool calls" in result.stdout

        unknown = tmp / "unknown.jsonl"
        write_jsonl(unknown, [
            {"type": "session_meta", "payload": {"id": "unknown"}},
            {"type": "response_item", "payload": {"type": "message", "role": "user", "content": "Inspect a file"}},
            {"type": "mystery_record", "payload": {}},
            {"type": "response_item", "payload": {"type": "function_call", "name": "shell", "arguments": "{\"command\":\"ls\"}", "call_id": "c1"}},
            {"type": "response_item", "payload": {"type": "function_call_output", "call_id": "c1", "output": "file.txt"}},
            {"type": "response_item", "payload": {"type": "message", "role": "assistant", "content": "done"}},
        ])
        result = run("python3", str(PREFLIGHT), str(unknown), "--harness", "codex",
                     "--confirm-private", ok=False)
        assert "unknown skipped records" in result.stdout

    run("python3", str(VALIDATE), str(PUBLIC_REPORT))
    print("Evaluator entrypoint regressions passed.")


if __name__ == "__main__":
    main()
