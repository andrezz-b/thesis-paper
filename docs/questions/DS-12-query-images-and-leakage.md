---
id: DS-12
title: How are query images selected, and how is leakage prevented?
area: dataset
status: open
phase: dataset
priority: medium
depends_on: []
informs: [IX-01, RP-01]
---

## Question

Which Commons photo becomes the query image for an entity, which quality rules apply,
and how is it ensured that the image or its metadata does not give the answer away?

## Why it matters

If the query image is identical to the index image, retrieval becomes trivial. If the
photo shows the name, the task becomes reading text.

## Notes

- Decided: query images are Wikimedia Commons photos of the same entity, different
  from the image in the index; Commons licences are followed and attributions are
  generated ([D-005](../decisions.md#d-005)).
- Open:
  - Source of candidates: P18 vs the entity's Commons category vs Commons
    structured data ("depicts", P180).
  - Quality filters.
  - Entities with only one image: probably excluded.
  - Near-duplicate photos (e.g. perceptual hash).
  - Visible text or logos naming the entity.
  - File names and captions must never reach the agent.
- 2026-11-07: ReasonVQA takes images from Visual Genome (objects linked to Wikidata via WordNet synsets) and Google Landmarks v2 (annotated with Wikimedia URLs that lead to Wikidata entities) (§3.1, App. 1.2). Licences of these images are not discussed in the paper. Source: [ReasonVQA note](../literature/tran2025reasonvqa.md).

## Resolution

_Not resolved yet._
