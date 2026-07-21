#!/usr/bin/env python3
"""Fail when a maintained public Markdown page links to a missing local target."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
SKIP_PARTS = {"experiments", "traces", "scaffolds"}


def pages():
    roots = [ROOT / "README.md", ROOT / "CLAUDE.md", ROOT / "docs", ROOT / "evals" / "README.md"]
    roots += [ROOT / "evals" / "agent-harness", ROOT / "evals" / "regeval" / "README.md"]
    found = []
    for item in roots:
        if item.is_file():
            found.append(item)
        elif item.is_dir():
            found.extend(item.rglob("*.md"))
    return sorted({p for p in found if not SKIP_PARTS.intersection(p.parts)})


def main():
    errors = []
    for page in pages():
        for target in LINK.findall(page.read_text(encoding="utf-8")):
            target = target.split("#", 1)[0].strip().strip("<>")
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            resolved = (page.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"{page.relative_to(ROOT)} -> {target}")
    if errors:
        raise SystemExit("Missing local Markdown links:\n" + "\n".join(errors))
    print(f"Markdown links passed ({len(pages())} maintained pages).")


if __name__ == "__main__":
    main()
