---
id: DS-07
title: Can the image show an entity other than the subject of the question?
area: dataset
status: researching
phase: dataset
priority: low
depends_on: [DS-05]
informs: []
---

## Question

Should some questions use an image of a related entity, e.g. a manufacturer's logo
with a question about one of its products?

## Why it matters

Adds an extra grounding hop and a different kind of difficulty. The user finds it
interesting to explore.

## Notes

- Not decided; exploratory.
- 2026-11-12: RETINA (Lee et al., 2025) is a precedent: the image depicts a related entity and the question asks about the answer entity; the 2k curated test set and the Table 1 drop (e.g. MuKA Recall@5 8.6 on unseen) show this is harder (Sec. 3, 5.2). User: increasingly likely to be used, an option adapted to Wikidata, where the related entity is a graph neighbour of the answer entity and the gold query is built from the graph (leaning, not decided). Source: [Lee et al. note](../literature/lee2025breaking.md).

## Resolution

_Not resolved yet._
