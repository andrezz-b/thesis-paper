---
id: DS-05
title: What role does the image play; is it always the single subject entity?
area: dataset
status: researching
phase: dataset
priority: medium
depends_on: []
informs: [DS-01, DS-06, DS-07]
---

## Question

Does the image always show exactly one Wikidata entity that is the subject of the
question ("this phone"), or are other roles allowed?

## Why it matters

Defines the visual axis of the dataset and what the image tool has to support.

## Notes

- Current assumption (tentative): mostly one entity, which is the subject of the
  question. To be verified and explored.
- Other roles:
  - the image shows a related entity rather than the subject ([DS-07](DS-07-related-entity-images.md));
  - several images or entities ([DS-06](DS-06-multi-image-questions.md), stretch goal);
  - the answer depends on visual attributes (colour, count, text in the image). This
    has not been discussed yet.
- 2026-11-04 (supervisor meeting, user's notes): idea that the image could be more
  complex, with other things in it, e.g. "What is the object that the person is
  holding in their right hand?". Exploratory, not a decision; the current
  assumption stays. It is a possible difficulty axis ([DS-13](DS-13-difficulty-levels.md)); visual knowledge
  graph papers may help ([LIT-05](LIT-05-visual-knowledge-graphs.md)).
- 2026-11-07: M3-VQA has images with several visual entities (paper §3, Table 2), the same idea as the multi-entity direction above. Stretch, not committed. Source: [M3-VQA note](../literature/ma2026m3.md).
- 2026-11-07: ReasonVQA questions about Visual Genome images refer to one object among others via scene-graph context ("the appliance on the street", "the keyboard instrument next to the table"), a possible model for the "more complex image" idea (§3.2.1, demo). Also see [LIT-05](LIT-05-visual-knowledge-graphs.md). Source: [ReasonVQA note](../literature/tran2025reasonvqa.md).
- 2026-11-12: RETINA builds questions where the query image shows a related entity of the answer document, not its main entity, and shows existing retrievers drop sharply (Table 1, Sec. 1). Closest precedent for the "image shows another entity" role. Source: [Lee et al. note](../literature/lee2025breaking.md).

## Resolution

_Not resolved yet._
