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

## Resolution

_Not resolved yet._
