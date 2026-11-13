---
id: IX-04
title: What does the index store per entity?
area: index
status: researching
phase: dataset
priority: low
depends_on: []
informs: [AG-02]
---

## Question

Which payload is stored with each vector (QID only, label, description), and how many
images per entity go into the index?

## Why it matters

Determines what the image tool returns to the agent.

## Notes

- Leaning: QID only. The agent can look up labels through SPARQL.
- POC payload: `{ qid, label, image }`. Answers are never stored in the index (see
  the conventions in the POC's
  [AGENTS.md](https://github.com/andrezz-b/thesis-dataset-poc/blob/main/AGENTS.md)).
- 2026-11-07: M3-VQA stores per entity the Wikipedia summary and the first page image (image corpus), plus at least 3 page sections (text corpus) (paper App. D.3, F.4). Source: [M3-VQA note](../literature/ma2026m3.md).
- 2026-11-08: OVEN's entity representation is the name (text) plus the first infobox image; a black image when the entity has none (§2 footnote 2, §3, §5.1). Infobox images exist for 2,032,340 of 6,063,945 entities. Source: [OVEN note](../literature/hu2023open.md).
- 2026-11-13: KnowCoL represents an entity by its Wikipedia description plus the mean embedding of its lead images, falling back to the text embedding when there is no image (Eq. 4, 5, 12). Contrasts with the QID-only payload we lean towards. Source: [KnowCoL note](../literature/zhou2025seeing.md).

## Resolution

_Not resolved yet._
