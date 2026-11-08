---
id: IX-03
title: Which image embedding model(s) are used for the index?
area: index
status: researching
phase: dataset
priority: low
depends_on: []
informs: [RP-05]
---

## Question

Is CLIP ViT-B/32 (as in the POC) kept, and are other models compared?

## Why it matters

The embedding model sets retrieval quality and therefore the ceiling for the
index-based agent configurations.

## Notes

- The POC uses `Xenova/clip-vit-base-patch32` through `@huggingface/transformers`, on
  CPU in Node
  ([`embeddings/clip.js`](https://github.com/andrezz-b/thesis-dataset-poc/blob/main/embeddings/clip.js)).
- Comparing several models (e.g. larger CLIP variants, SigLIP) is a nice-to-have if
  there is time.
- 2026-11-07: M3-VQA indexes each entity as the sum of the CLIP ViT-L embeddings of its article summary and its image; this beat either alone and name + image in their preliminary experiments (paper App. F.4). Source: [M3-VQA note](../literature/ma2026m3.md).
- 2026-11-08: OVEN baselines use CLIP ViT-L14. Vanilla CLIP is weak over 6M entities (test overall hm 2.4); CLIP2CLIP, which combines image/text similarities between query and entity, reaches 5.3 (Table 2). Retrieval-style CLIP models do relatively better on tail entities (<2.5K monthly page views, Fig. 6). Different setting (6M candidates, fine-tuned), so not directly comparable to our small index. Source: [OVEN note](../literature/hu2023open.md).

## Resolution

_Not resolved yet._
