# RegEval research goal

## Question

Can an LLM judge classify regulated-domain responses consistently with a human-labelled
reference set while exposing dangerous false-clear errors and abstention behavior?

## Fixed measurement contract

- Primary metric: Cohen's kappa.
- Diagnostics: TPR, TNR, abstention rate, coverage, and false-clear count.
- Intervention: one scaffold change per experiment.
- Record: keep/discard decision plus an append-only explanation.
- Promotion: a separate uncontaminated verification set must clear a predeclared bar.

## Public reproducibility boundary

The public synthetic dataset exercises the scorer but does not substantiate domain-quality
claims. The later 36-item held-out dataset is private and is not included. Historical numbers
that depend on it are preserved as research history, not presented as independently
reproducible evidence.

The unattended driver described in early notes never became a releasable public product. The
current repository therefore treats autoresearch as a design case study until both a safe
driver and a releasable dataset exist.
