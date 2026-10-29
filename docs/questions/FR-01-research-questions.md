---
id: FR-01
title: What are the research questions and hypotheses?
area: framing
status: open
phase: dataset
priority: medium
depends_on: [LIT-01]
informs: [FR-02, DS-01, EV-02, EV-03]
---

## Question

What exactly does the thesis ask or claim, and which hypotheses are tested?

## Why it matters

Decides which question types, configurations and ablations are worth the effort and
what the evaluation has to show. Also needed for the project plan and the title.

## Notes

- The framing is decided: agentic text-to-SPARQL extended to images ([D-001](../decisions.md#d-001)).
- The user expects some hypotheses but none are defined yet.
- Candidate directions (not agreed, only suggestions so far):
  - how accuracy changes with the number and similarity of distractors ([IX-02](IX-02-distractor-count.md));
  - how accuracy changes with hop count and question type ([DS-01](DS-01-question-types.md), [DS-03](DS-03-hop-depth.md));
  - how much an image-retrieval tool adds compared to a vision-capable model that
    recognises the entity itself ([AG-05](AG-05-experiment-configurations.md)).
- The contribution statement depends on what the closest related work already covers
  ([LIT-01](LIT-01-existing-image-sparql-benchmarks.md)).

## Resolution

_Not resolved yet._
