---
id: DS-03
title: What is the maximum number of hops in a question?
area: dataset
status: open
phase: dataset
priority: medium
depends_on: [DS-01, DS-02]
informs: []
---

## Question

Up to how many hops (from the depicted entity to the answer) should questions go?

## Why it matters

Limits generation effort and query complexity; hop count is a natural axis for
reporting results.

## Notes

- The user has no preference yet.
- ReasonVQA uses 1–3 hops. The POC examples are 2–3 hops (e.g.
  [Game Boy](https://github.com/andrezz-b/thesis-dataset-poc/tree/main/examples/game-boy):
  `manufacturer → founded by → date of birth`).
- Recognising the entity from the image is an extra grounding step before the first
  hop.
- 2026-11-04 (supervisor meeting): hop count is one candidate difficulty axis and a label per item; see [DS-13](DS-13-difficulty-levels.md) and [DS-14](DS-14-question-labels.md).

## Resolution

_Not resolved yet._
