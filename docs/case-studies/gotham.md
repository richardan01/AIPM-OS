# Gotham agent-system case study

The original AI Product Lab used eight Batman-character agents as a memory device for clear
ownership: strategy, operations, building, research, writing, adversarial review, technical
coaching, and reader-voice review.

The useful design pattern was not the theme. It was the separation of responsibilities:

- every agent had one job and explicit handoffs;
- author and reviewer roles were different contexts;
- public artifacts required adversarial and reader-voice approval;
- a quarterly thesis constrained what the system was allowed to optimize.

The full prompts and operating system made the public repository difficult to navigate, so
they are no longer active on `main`. They remain inspectable in the immutable
[`ai-product-lab-os-v1`](https://github.com/richardan01/AI-Product-Lab/tree/ai-product-lab-os-v1)
snapshot.

The current repository keeps the same strongest principle—separate authoring from grading—
without requiring visitors to learn the Gotham vocabulary.
