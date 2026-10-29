---
id: DS-02
title: Which part of Wikidata is well connected enough to build the dataset on?
area: dataset
status: open
phase: dataset
priority: high
depends_on: []
informs: [DS-03, DS-09, IX-01]
---

## Question

Which domains or classes of Wikidata should the dataset be built on, and how is "well
connected" measured?

## Why it matters

Multi-hop and aggregate questions need entities with many complete outgoing paths; the
image index needs entities with images. Everything downstream (distractors,
generation) depends on the chosen domains.

## Notes

- User's criteria: mainly hop paths (enough multi-hop paths from the depicted
  entity); image coverage (P18) is a good secondary criterion.
- No explicit domain exclusions (people are not excluded a priori).
- The POC used product models (chairs, game consoles, cell phones, laptops) with
  paths like `manufacturer (P176) → inception (P571)`; see the
  [POC README](https://github.com/andrezz-b/thesis-dataset-poc/blob/main/README.md).
- Candidate measures per class: share of instances with P18; number of Commons images
  per entity (each needs at least an index image and a different query image, see
  [DS-12](DS-12-query-images-and-leakage.md)); number of distinct property paths of length 1–3; completeness of key
  properties; class size (for distractors, [IX-01](IX-01-distractor-strategy.md)).
- Approach: aggregate SPARQL statistics per candidate class (QLever is fast for this;
  see [DS-04](DS-04-endpoint-snapshot.md)). Question types ([DS-01](DS-01-question-types.md)) tell which path shapes are needed.

## Resolution

_Not resolved yet._
