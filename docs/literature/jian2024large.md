---
key: jian2024large
title: "Large Language Models Know What is Key Visual Entity: An LLM-assisted Multimodal Retrieval for VQA"
authors: ["Pu Jian", "Donglei Yu", "Jia-Jun Zhang"]
year: 2024
venue: "Conference on Empirical Methods in Natural Language Processing"
url: "https://doi.org/10.18653/v1/2024.emnlp-main.613"
pdf: "https://aclanthology.org/2024.emnlp-main.613.pdf"
arxiv: ""
doi: "10.18653/v1/2024.emnlp-main.613"
s2_id: "fc48dd4a5873f0736b397855a832004882610131"
code: ""
data: ""
status: reviewed
relevance: medium
read_depth: full
informs: [AG-02, AG-05, DS-05, DS-13, IX-03, EV-03]
themes: [vqa, agentic-sparql]
added: 2026-11-21
reviewed: 2026-11-21
candidates:
  - id: "arXiv:2601.19060"
    title: "PixSearch: Region-Grounded Retrieval for Knowledgeable Large Multimodal Models"
    via: cites
    priority: high
    why: "Region-centric retrieval that uses detector or grounding outputs as query crops, explicitly building on LLM-RA; closest to an image-side crop tool for AG-02, DS-05 and IX-03 (abstract and citing sentences)."
  - id: "arXiv:2509.00798"
    title: "Progressive Multimodal Search and Reasoning for Knowledge-Intensive Visual Question Answering"
    via: cites
    priority: high
    why: "Multi-step multimodal search and reasoning for KI-VQA with a revision mechanism, compared against LLM-RA on InfoSeek; fits AG-02 and AG-05 (abstract only)."
bibtex: |
  @inproceedings{jian2024large,
    title={Large Language Models Know What is Key Visual Entity: An LLM-assisted Multimodal Retrieval for VQA},
    url={http://dx.doi.org/10.18653/v1/2024.emnlp-main.613},
    DOI={10.18653/v1/2024.emnlp-main.613},
    booktitle={Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing},
    publisher={Association for Computational Linguistics},
    author={Jian, Pu and Yu, Donglei and Zhang, Jiajun},
    year={2024},
    pages={10939–10956}
  }
---

# Large Language Models Know What is Key Visual Entity: An LLM-assisted Multimodal Retrieval for VQA

## TL;DR

LLM-RA is a retrieval-augmented VQA system whose retriever query is built from the "key visual entities" of the image instead of the whole image. An LVLM captions the image, an LLM picks the entities the question is about from caption plus question, and a grounding model crops their regions (ROIs). Each ROI is encoded separately for retrieval over Wikipedia passages. Removing the irrelevant image content raises Recall@5 on OK-VQA and InfoSeek (Tables 1, 2, 4). For us it is a recipe for an image-side tool (question-aware entity extraction and cropping before image-index search), not a KGQA paper.

## Problem and contribution

- Problem: RA-VQA retrievers encode the whole image, so entities that matter for the question are drowned by irrelevant content ("person", "road"), and one pooled query vector makes entities interfere with each other (§1, Fig. 1).
- Contribution (§1): (1) LLM-RA, an LLM-assisted multimodal retrieval method that emphasises question-relevant key visual entities; (2) a comparison of ways to use the visual features for retrieval, where key-entity ROIs perform best (§5.2, §5.3, Table 4).

## Method

Two stages (§3, Fig. 2); the answer generator is the existing RA-VQA one of Lin and Byrne (2022).

1. Key visual entity extraction (§3.1):
   - An LVLM (MiniGPTv2, §4.1) writes a detailed caption.
   - An LLM (the frozen LLM of MiniGPTv2, §4.1) gets the question and caption with in-context examples and outputs entities and attributes as `{"entity": "attribute"}`. Instruction: "Given a description of an image, output the entities that the question might focus on" (§3.1, prompt in Appendix A).
   - Visual grounding: each pair becomes a referring expression "The {entity} that {attribute}" and Grounding-DINO (referring expression comprehension model, §4.1) returns the ROI (§3.1).
2. Multimodal joint retrieval (§3.2):
   - The question, the whole image and each ROI are encoded separately (ColBERTv2 text encoder, CLIP ViT-base image encoder plus a visual mapping network). The embeddings are concatenated into one multi-vector query (Eq. 1).
   - Late-interaction (ColBERT) similarity, summed over query vectors of the max over document tokens (Eq. 3). Documents are indexed with FAISS (§4.1).
   - Training: the visual mapping network is pretrained contrastively on Wikipedia image-text pairs (following Lin et al. 2024a); the retriever is trained with contrastive loss, the answer generator is fine-tuned with LoRA (§3.2, §4.1).

Referring expression comprehension (REC): given an image and a text phrase describing one object, the model returns the box of that object (assistant reading; the paper only cites Liu et al. 2023b, Grounding-DINO). It is open-vocabulary detection by text, not segmentation. A similar detect-and-crop step is the object detection tool of the M³-VQA agent ([ma2026m3](ma2026m3.md), §5.4, App. F.5).

## Data / benchmark

Not a dataset paper. It evaluates on two existing KI-VQA benchmarks (§4.2):

- OK-VQA: no gold documents; Google Search corpus (~170K passages), documents containing the answer count as positives.
- InfoSeek: 100K-passage Wikipedia knowledge base (the ~7K gold passages plus random ones from the 6M).
- Metrics: Recall@K, VQA Score, EM, InfoSeek Score (§4.3).
- No SPARQL, no knowledge graph; a text passage corpus. Not checked: licence, splits (they follow the original benchmarks).

## Key results

- OK-VQA: Recall@5 90.37, VQA Score 63.29, EM 68.31, above RA-VQAv2 (61.86 VQA Score) (Table 1).
- InfoSeek: Infoseek Score 23.14 vs 22.1 for PaLI-X (Table 2 and §5.1).
- Ablation, without key-entity ROIs: Recall@5 drops from 90.37 to 87.24 (OK-VQA) and from 47.31 to 39.78 (InfoSeek) (Tables 1, 2). Without independent encoding (summing everything into one vector): 85.83 and 37.52 (Tables 1, 2).
- More objects in the image, bigger gain: without key entities Recall@5 falls from 88.75 (1-3 objects) to 86.13 (9+) on OK-VQA and from 41.59 to 37.12 on InfoSeek; with them it stays at about 90 and 47 (Table 3).
- ROI strategies on Recall@5 (Table 4): none 87.24 / 39.78 (OK-VQA / InfoSeek), random crops 87.02 / 38.29, evenly split 87.14 / 38.63, all detected objects 88.29 / 41.78, ROIs from the question alone 88.03 / 43.45, LLM-RA 90.30 / 47.31.
- Pipeline beats end-to-end grounding with Shikra (Shikra-GCoT 88.17 / 41.93 vs 90.30 / 47.31) (Table 5, §5.3).
- On 400 sampled questions the authors judged 54 (OK-VQA) and 98 (InfoSeek) "complex" (Table 6). On these, Recall@5 goes from 64.81 to 81.48 and from 21.43 to 44.90 (Table 7).

## Limitations

Authors say (Limitations):

- No LLM above 13B was tried (7B used).
- Only the retriever is improved, not answer generation.
- OK-VQA and InfoSeek contain few questions that need both cross-modal reasoning and long-tail knowledge.

We see (assistant reading):

- Several components have to be trained (visual mapping network, retriever, LoRA generator), so this is not a plug-in recipe.
- Three models are chained (captioner, LLM, grounder); no evaluation of errors in the entity extraction step itself is reported. Not checked in the appendix.
- Ablations measure Recall@5 against Google Search passages whose positives are defined by answer string match; the authors note that this may understate the OK-VQA gain (§5.2).

## Relevance to the thesis

Proposed, to be agreed with the user:

- [AG-02](../questions/AG-02-tool-set.md): cite. LLM-RA shows that cropping the key-entity regions before retrieval improves it (Tables 1, 2, 4). We would take the crop idea from M³-VQA (`ma2026m3`), whose agentic detection and per-segment image retrieval (§5.4) fits our agent approach better. LLM-RA adds many components (caption model, entity-extraction prompt, grounder, trained retriever) that raise complexity (§3).
- [AG-05](../questions/AG-05-experiment-configurations.md): the paper compares whole-image against key-ROI queries (Table 4), which maps to a "whole image" vs "cropped entity" configuration for the index search.
- [EV-03](../questions/EV-03-ablations.md): possible ablation, only if we adopt the crop approach (most likely via M³-VQA): whole-image vs cropped-entity queries to the index, as in Table 4.
- [DS-13](../questions/DS-13-difficulty-levels.md) / [DS-05](../questions/DS-05-image-role.md): cite. Retrieval quality falls with the number of objects (Table 3) and their "complex" samples do not name the entity (§5.3), which supports multi-object query images as a difficulty axis.
- [IX-03](../questions/IX-03-embedding-models.md): contrast. They use CLIP image features, but with a pretrained mapping network and late-interaction retrieval (§3.2); our fixed CLIP index search per crop is a simpler variant (training is out of scope, [D-008](../decisions.md#d-008)).
- [LIT-01](../questions/LIT-01-existing-image-sparql-benchmarks.md): not relevant, no KG or SPARQL; text-passage RA-VQA.

## Citable claims

- In RA-VQA, redundant image content irrelevant to the question hides the key entities from the retriever (§1, Fig. 1).
- Using an LLM to pick question-relevant entities from an image caption, then grounding them to ROIs, gives better retrieval than using no ROIs, random or evenly split crops, all detected objects, or entities parsed from the question alone (§5.3, Table 4).
- The retrieval gain from key entities grows with the number of objects in the image (§5.3, Table 3).
- Encoding each ROI independently beats summing all features into one query vector (§5.2, Tables 1, 2).
- A pipeline of mature components (caption, LLM, grounding model) outperformed an end-to-end grounding VLM (Shikra) in their setup (§5.3, Table 5).

## My notes
- Key visual entity extraction
	- Large visual-language models (LVLMs) caption the image
	- LLMs use the generated caption and the question to determine key entities along with their attributes
	- Visual Grounding - based on entities and attributes determine regions of interest (ROI) corresponding to those entities (similar to the detect-and-segment step in the agent of [M³-VQA](ma2026m3.md))
- Multimodal joint retrieval
	- Interesting approach but includes pretraining so I think it would go out of the scope of the thesis unless we find a pretrained model
- Using no entity extraction causes worse recall, the recall performance falls as the amount of objects/entities increases (Table 3)
- LLM extraction outperforms other ROI methods
## Open doubts

- Not read: Appendices A to C (prompt, questionnaire, implementation details).
- How often does the LLM pick the wrong entity, and how does the grounder fail on fine-grained entities? Not reported in the main text.
- Does a frozen CLIP index (no mapping-network pretraining) keep the gain from per-crop queries? Not tested here.
