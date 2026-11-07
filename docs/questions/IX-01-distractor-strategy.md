---
id: IX-01
title: How are distractor images chosen for the image index?
area: index
status: researching
phase: dataset
priority: high
depends_on: [DS-02]
informs: [IX-02]
---

## Question

Which entities are added to the shared image index as distractors (noise) besides the
gold entities?

## Why it matters

Distractors decide how hard image grounding is. They can also serve as an evaluation
axis ([IX-02](IX-02-distractor-count.md), [FR-01](FR-01-research-questions.md)).

## Notes

- Initial idea: images of entities in the same or a closely related category.
- Options: same class (P31), sibling or parent classes, nearest neighbours in
  embedding space (hard negatives), random.
- Decided: one shared index ([D-006](../decisions.md#d-006)). The gold entities of one question then also act
  as distractors for the others.
- POC: 26 entities per example (1 gold + 25 of the same class). For the
  [egg chair](https://github.com/andrezz-b/thesis-dataset-poc/tree/main/examples/egg-chair)
  the gold entity was not in the top 5, which shows how hard look-alike distractors are.
- 2026-11-07: M3-VQA adds about 5 hard negatives per entity: embed Wikipedia summaries (all-mpnet-base-v2), take the 20 nearest with FAISS, sample 5 at random; retrieval runs over the whole constructed knowledge base (paper App. D.3). The similarity is textual, not visual. Leaning (user, not decided): choose distractors that are `instance of` the same class; text-similarity neighbours could be an additional distractor source. Source: [M3-VQA note](../literature/ma2026m3.md).

## Resolution

_Not resolved yet._
