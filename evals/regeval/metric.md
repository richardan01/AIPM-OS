# RegEval metric: Cohen's kappa

RegEval optimizes one metric: Cohen's kappa between judge predictions and human reference
labels. Accuracy alone can look strong on an imbalanced dataset; kappa adjusts observed
agreement for agreement expected from the two label distributions.

```text
kappa = (observed agreement - expected agreement)
        / (1 - expected agreement)
```

The current task is binary: `compliant` or `non-compliant`. The earlier `unclear` gold class
was quarantined after poor inter-annotator agreement. If a binary judge emits `unclear`, the
scorer forces it to an error so abstention cannot inflate the result.

## Diagnostics

Every score should be read with:

- TPR, to catch an always-rejecting judge;
- TNR, to catch an always-accepting judge;
- abstention rate;
- sample size and prediction coverage;
- a seeded bootstrap confidence interval;
- the judge model and harness used.

The historical keep threshold was kappa >= 0.80 with a confidence-interval lower bound >=
0.70. These are experiment rules, not a universal statement that a judge is safe to deploy.

## Public boundary

The `demo/` data is synthetic and exists only to exercise `score.py`. The private later
held-out dataset is not shipped, so claims based on it are not reproducible from this clone.
Read the [discovery pass](discovery-pass-2026-06-28.md) for the contamination correction.
