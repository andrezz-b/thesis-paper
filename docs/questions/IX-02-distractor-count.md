---
id: IX-02
title: How many distractors should the index contain?
area: index
status: researching
phase: dataset
priority: medium
depends_on: [IX-01]
informs: []
---

## Question

How many distractor images per gold entity (or in total), and should several levels
be evaluated?

## Why it matters

Too few and grounding is trivial; too many and the index is expensive to build.
Varying the amount could become an ablation or research question.

## Notes

- The user has no preference yet.
- 2026-11-08: OVEN has no curated distractor set: every other KB entity (6M) is a candidate. CLIP2CLIP accuracy falls roughly linearly in log candidate count from 20K to 6M, while PaLI is flatter (§6, Fig. 5). How the negatives are sub-sampled is not stated. Supports varying the distractor count as an experiment axis. Source: [OVEN note](../literature/hu2023open.md).

## Resolution

_Not resolved yet._
