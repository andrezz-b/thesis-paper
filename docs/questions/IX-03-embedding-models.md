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
- 2026-11-21: LLM-RA uses a CLIP ViT-base image encoder with a visual mapping network pretrained on Wikipedia image-text pairs and ColBERT-style late interaction (§3.2), i.e. trained components; our fixed embedding index without training is a simpler variant, and the paper does not test frozen CLIP alone for crop queries. No change to the plan. Source: [LLM-RA note](../literature/jian2024large.md).
- 2026-11-21: PMSR uses SigLIP2 for images and Qwen3-Embedding for text, and scores image-KB hits as 0.5 · text similarity + 0.5 · image similarity of the input image (§3.3, Eq. 7; App. D). On E-VQA, image+text beats image-only (R@5 43.1 vs 36.2, App. D, Table A1); a larger SigLIP2/Qwen3-Embedding pair beats a smaller one (BEM 45.5 to 47.1 for Qwen3-VL-8B, App. J). Only noted as what they use; a 2M-pair Wikipedia KB, not comparable to our small index. Source: [PMSR note](../literature/choi2025progressive.md).
- 2026-11-22: SAGE-VQA searches its KG image index with frozen CLIP embeddings of verified crops (2 nearest images per crop, FAISS; App. A.7), with no training, which matches our simpler fixed-index variant. It does not compare embedding models. No change to the plan. Source: [SAGE-VQA note](../literature/shen2026sage.md).

## Resolution

_Not resolved yet._
