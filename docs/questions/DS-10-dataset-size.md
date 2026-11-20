---
id: DS-10
title: How large should the dataset be?
area: dataset
status: open
phase: dataset
priority: medium
depends_on: [DS-09]
informs: []
---

## Question

What is the minimum viable size, and what is the target if things go well?

## Why it matters

Needs to be large enough for per-type results while fitting the dataset freeze on
2027-01-22 ([D-015](../decisions.md#d-015)).

## Notes

- The user expects this to depend on progress and remaining time.
- Reference sizes: SPINACH 320 questions; KGVoyager's benchmarks 14–100 questions
  each; WikiVQABench 344 questions.
- 2026-10-30: The questions are curated manually ([D-016](../decisions.md#d-016)), so the reachable size is
  limited by curation time and smaller than with automatic generation.
- 2026-11-06: SPINACH: 155 dev + 165 test; its dev set separates systems that differ by at least 9.0% EM (minimum detectable effect, App. C.2). Source: [SPINACH note](../literature/liu2024spinach.md).
- 2026-11-15: Encyclopedic-VQA uses variety (unique bigrams over questions, 257.9k there) and disparity (mean pairwise Sentence-BERT cosine distance, 0.833) to compare question diversity (§4.5, Table 3). Variety grows with dataset size; disparity is a possible measure for a small curated set (user: possible idea, not decided). Source: [Encyclopedic-VQA note](../literature/mensink2023encyclopedic.md).

## Resolution

_Not resolved yet._
