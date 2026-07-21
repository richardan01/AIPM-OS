# RegEval autoresearch design

This page records the experiment design, not a runnable unattended system.

The useful pattern borrowed from Karpathy's autoresearch is deliberately small:

1. Freeze the task, labels, metric, and experiment budget.
2. Change one judge scaffold at a time.
3. Score the candidate against the same tuning set.
4. Keep, hold, or discard it using a predeclared threshold.
5. Append the outcome and rationale; never rewrite failed history.
6. Promote only after a separate, uncontaminated verification set passes.

The public repository ships the scorer and historical experiment record. It does **not** ship
an unattended driver or the private later held-out dataset. Therefore RegEval autoresearch is
a documented design and case study, not a command visitors should leave running.

Use the small synthetic demo in [README.md](README.md) to exercise the scorer safely. Use the
[contamination discovery](discovery-pass-2026-06-28.md) to study why fixed data boundaries and
append-only experiment history matter.
