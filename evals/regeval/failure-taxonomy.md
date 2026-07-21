# RegEval failure taxonomy

The case study became useful when it named measurement failures instead of reporting only a
headline score.

| Failure | Why it matters | Response |
|---|---|---|
| False clear | Judge accepts a genuinely non-compliant item | Treat as the highest-risk error; inspect examples before promotion |
| False flag | Judge rejects a compliant item | Measure with TPR/TNR and inspect prompt strictness |
| Hedge | Judge emits `unclear` on a decidable binary item | Count it as an error in binary mode |
| Class collapse | Judge predicts mostly one label | Read kappa beside class-specific recall |
| Gold-label defect | Human reference is ambiguous or wrong | Re-adjudicate; record the correction without rewriting past runs |
| Harness drift | Model or invocation mode changes between runs | Pin and log both; do not compare unlike runs directly |
| Held-out contamination | Verification items overlap tuning data | Invalidate the claim and rebuild a disjoint set |
| Metric shopping | Success definition changes after results are visible | Freeze one primary metric and keep/discard rule before the run |

The held-out contamination and weak `unclear` agreement are documented in the
[2026-06-28 discovery pass](discovery-pass-2026-06-28.md). The append-only
[experiment log](experiments/log.md) preserves the correction instead of erasing it.
