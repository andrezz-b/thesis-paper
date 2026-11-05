---
id: RP-03
title: What is the dataset record format?
area: repo
status: open
phase: dataset
priority: medium
depends_on: [DS-01, DS-08]
informs: []
---

## Question

What fields does a dataset record have, and in which file format?

## Why it matters

The format is the interface between the dataset pipeline and the agent and evaluation
code.

## Notes

- Suggestion: JSONL with a schema (the POC validates with zod, see
  [`lib/schema.js`](https://github.com/andrezz-b/thesis-dataset-poc/blob/main/lib/schema.js)).
- Candidate fields: id, question text, query image reference(s), gold entity QID(s),
  gold SPARQL, gold result with snapshot date, question type label(s), hop count,
  split, attribution.
- 2026-11-04 (supervisor meeting): question labels (hops, type, others) are to be
  defined in [DS-14](DS-14-question-labels.md); difficulty in [DS-13](DS-13-difficulty-levels.md).

## Resolution

_Not resolved yet._
