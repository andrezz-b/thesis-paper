---
id: DS-01
title: Which question types will the dataset contain?
area: dataset
status: open
phase: dataset
priority: high
depends_on: [LIT-02]
informs: [DS-02, DS-03, DS-06, DS-09, DS-11, RP-03]
---

## Question

Which question types (and along which axes) does the dataset cover, and roughly in
what proportions?

## Why it matters

Drives which part of Wikidata is suitable ([DS-02](DS-02-wikidata-subset.md)), the hop depth ([DS-03](DS-03-hop-depth.md)), the
generation pipeline ([DS-09](DS-09-generation-pipeline.md)) and the record format ([RP-03](RP-03-dataset-format.md)).

## Notes

- Initial ideas (before research): first order / single-hop, multi-hop, comparison,
  yes/no, list, count. To be formalised from [LIT-02](LIT-02-question-type-taxonomy.md).
- Decided: the depicted entity is never named in the question ([D-004](../decisions.md#d-004)).
- Comparison questions need two entities. With one image, the second has to be named
  in the text or come from a second image (multi-image is a stretch goal, [DS-06](DS-06-multi-image-questions.md)).
- Possibly quotas per type, so results can be reported per type.

## Resolution

_Not resolved yet._
