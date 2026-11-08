---
id: LIT-04
title: How do related works choose distractors for visual entity retrieval?
area: literature
status: researching
phase: dataset
priority: medium
depends_on: []
informs: [IX-01]
---

## Question

How do visual entity linking and knowledge-based VQA works build their image
candidate sets and hard negatives?

## Why it matters

Gives a citable basis for the distractor strategy of the image index ([IX-01](IX-01-distractor-strategy.md)).

## Notes

Starting points (to verify):

- KVQA: reference images of 69K persons harvested from Wikidata for one-shot visual
  entity linking.
- Open-domain visual entity recognition (OVEN, Hu et al. 2023, arXiv 2302.11154),
  used by InfoSeek (read, see below).
- Wiki-VEL: visual entity linking for structured data on Wikimedia Commons (2024).
- Cross-modal retrieval for knowledge-based VQA (Lerner et al., ECIR 2024; CLIP-based).
- 2026-11-07: M3-VQA (paper App. D.3) is a further starting point: about 5 text-similarity hard negatives per entity in a controlled multimodal knowledge base. Source: [M3-VQA note](../literature/ma2026m3.md).
- 2026-11-07: KVQA's open world uses reference images of 69K persons as the identity pool; QA accuracy drops by more than 10 points versus the closed world (18K), which the authors attribute partly to distractors (§Approach, p. 8883). Distractors are all other identities, not selected by similarity. Source: [KVQA note](../literature/shah2019kvqa.md).
- 2026-11-08: InfoSeek's With-KB protocol uses a 100K Wikipedia KB with the benchmark entities plus top frequent Wikipedia entities (§4); no hard-negative selection is described. A pool of general frequent entities next to same-class distractors is an option for [IX-01](IX-01-distractor-strategy.md). Retrieval uses a fine-tuned CLIP2CLIP with an (image, question) query against (Wikipedia image, title) candidates, top-5 (§4.2); entity accuracy was 22.2 (Table 5). Source: [InfoSeek note](../literature/chen2023can.md).
- 2026-11-08: OVEN read ([note](../literature/hu2023open.md)): the KB (6M entities) is the distractor set, no hard-negative selection; accuracy falls with candidate-set size (§6, Fig. 5). Follow-ups on the same space (A Generative Approach for Wikipedia-Scale Visual Entity Recognition, arXiv 2403.02041) are queued as candidates.

## Resolution

_Not resolved yet._
