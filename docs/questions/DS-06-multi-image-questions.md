---
id: DS-06
title: How would multi-image questions work (stretch goal)?
area: dataset
status: open
phase: dataset
priority: low
depends_on: [DS-01, DS-05]
informs: []
---

## Question

If questions with several images are included, which types use them and how are they
represented?

## Why it matters

Multi-image questions are a stretch goal ([D-009](../decisions.md#d-009)). They fit comparison questions well
("which of these two companies was founded first?").

## Notes

- Pessimistic plan: only if time allows after the single-image dataset is done.
- The image tool must accept a reference to one specific image of the question, and
  retrieval runs once per image.

## Resolution

_Not resolved yet._
