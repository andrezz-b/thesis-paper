---
key: zhou2025seeing
title: "Seeing and Knowing in the Wild: Open-domain Visual Entity Recognition with Large-scale Knowledge Graphs via Contrastive Learning"
authors: ["Hong-Kuan Zhou", "Lavdim Halilaj", "Sebastian Monka", "Stefan Schmid", "Yuqicheng Zhu", "Jing-Cheng Wu", "Nadeem Nazer", "Steffen Staab"]
year: 2026
venue: "AAAI Conference on Artificial Intelligence"
url: "https://arxiv.org/abs/2510.13675"
pdf: "https://doi.org/10.1609/aaai.v40i16.38370"
arxiv: "2510.13675"
doi: "10.1609/aaai.v40i16.38370"
s2_id: "27074fa32c37448eca0da235ab96066d92402504"
code: ""
data: ""
status: reviewed
relevance: low
read_depth: full
informs: [LIT-01, IX-03, IX-04, AG-02]
themes: [visual-entity-recognition, kg-embeddings]
added: 2026-11-13
reviewed: 2026-11-13
candidates:
  - id: "arXiv:2402.18695"
    title: "Grounding Language Models for Visual Entity Recognition"
    via: refs
    priority: medium
    why: "AutoVER: retrieval-augmented constrained generation with an MLLM on OVEN; the closest to an agent-style approach to the identification step, and the strongest seen-entity baseline in Table 1 (abstract only)"
bibtex: |
  @article{zhou2025seeing,
    title={Seeing and Knowing in the Wild: Open-domain Visual Entity Recognition with Large-scale Knowledge Graphs via Contrastive Learning},
    volume={40},
    ISSN={2159-5399},
    url={http://dx.doi.org/10.1609/aaai.v40i16.38370},
    DOI={10.1609/aaai.v40i16.38370},
    number={16},
    journal={Proceedings of the AAAI Conference on Artificial Intelligence},
    publisher={Association for the Advancement of Artificial Intelligence (AAAI)},
    author={Zhou, Hongkuan and Halilaj, Lavdim and Monka, Sebastian and Schmid, Stefan and Zhu, Yuqicheng and Wu, Jingcheng and Nazer, Nadeem and Staab, Steffen},
    year={2026},
    month=Mar,
    pages={13638–13646}
  }
---

# Seeing and Knowing in the Wild: Open-domain Visual Entity Recognition with Large-scale Knowledge Graphs via Contrastive Learning

## TL;DR

KnowCoL is a dual-encoder (CLIP-based) model for OVEN: it embeds a Wikidata subgraph
with a translation-based KG embedding (TransE with cosine similarity), and trains the
(image + text query) encoder so that its output aligns with those node embeddings, with
the entities' Wikipedia text and lead images, as a contrastive objective. It reports
harmonic-mean top-1 accuracy of 38.8 on the OVEN entity test split, ahead of
the generative two-step baselines (Table 1). For us it is the contrasting, training-based use of
Wikidata for the identification step; our agent searches the graph and an image index at
inference time and trains nothing ([D-008](../decisions.md#d-008)).

## Problem and contribution

- Task: OVEN, linking an image plus a text query (the intent) to a Wikidata QID in an open,
  long-tailed label space where most entities are unseen in training (Intro, Problem Definition).
- Criticism of prior work: dual encoders treat entities as isolated labels; two-step generative
  methods (caption, then BM25 over names) lose information and are ambiguous (the "Mercury" example) (Intro).
- Contributions (Intro): (1) a dual-encoder approach using Wikidata and Wikipedia knowledge;
  (2) a study of which knowledge types and relations matter; (3) a gain of 10.5 points on unseen
  entities with a model 35x smaller than the previous best. The authors say they are the first to use a
  large-scale KG for open-domain visual entity recognition (Related Work).

## Method

- Backbone: frozen OpenCLIP image and text encoders, each with a trainable linear projection;
  the query image and the text query embeddings are fused (default: addition, Eq. 3, 13).
- Entity side: description text embedding, and the mean of the embeddings of the entity's
  Wikipedia lead images (falls back to the text embedding when there is no image) (Eq. 4, 5).
- Graph side: one learnable node embedding per entity and one embedding per relation (TransE,
  with cosine similarity and a cross-entropy loss instead of the margin loss) (Eq. 8-10, Appendix).
- Loss: L = alignment (query vs node embedding) + b1 proxy (node vs entity text/image
  embeddings) + b2 KE loss (triples around the entity, 50 per entity, 25 negatives) (Eq. 6, 7, 9, 11).
- Subgraph: triples between entities occurring in OVEN, plus their P31, P279 and P171 superclasses;
  32,122 entities, 501 relation types (Training details; Appendix, Structure Knowledge Extraction).
- Inference: argmax over entities of the similarity between the fused query embedding and
  the mean of the entity's text and image embeddings (Eq. 12). Assistant reading: the node embeddings
  do not appear in Eq. 12, so the KG only acts through training.

## Data / benchmark

Not a dataset paper; it is evaluated on OVEN only (Experiment Settings, "Our evaluation is
conducted solely on the OVEN benchmark"). Details of OVEN are in the [hu2023open](hu2023open.md) note.

- Seen / unseen: entities in / not in the OVEN training set; test split 15,888 entities (8,355 seen, 7,533 unseen).
- Metric: top-1 accuracy on seen and unseen, and their harmonic mean (HM) as the main metric.
- The paper states OVEN has "6,063,945 training samples", while the OVEN paper gives 6,063,945 entities (see Open doubts).
- Gold SPARQL: no. KG used: Wikidata subgraph as above. Agents: none evaluated.

## Key results

- OVEN entity test: KnowCoL-bigG (2.0B parameters) seen 41.8, unseen 36.1, HM 38.8; Auto-VER-14B 65.0 / 18.6 / 28.9; GER-ALD 29.1 / 16.3 / 20.9; PaLI-17B 28.3 / 11.2 / 16.0; CLIP2CLIP 12.6 / 10.5 / 11.4 (Table 1).
- Model size: KnowCoL-L 31.5, -H 35.8, -bigG 38.8 HM (Table 2). With the same ViT-L-14 backbone, KnowCoL-L reaches 31.5 against CLIP2CLIP's 11.4 (Table 2).
- Knowledge types (KnowCoL-L, Table 3): HM 31.5 full; 30.0 without lead images; 28.3 without hierarchical KG knowledge (P31, P279, P171), unseen 29.1 to 25.3.
- Fusion (Table 4): simple addition has the best HM (31.5); more complex fusers raise seen accuracy (TE + IP: 56.7) but lower unseen (17.9), i.e. overfit to seen entities.
- KGE method (Table 5): TransE + cosine 31.5, TransE + Euclidean 31.0, TransH 31.2, DistMult 30.9.
- Auto-VER is better on seen entities (65.0 vs 41.8) but worse on unseen (18.6 vs 36.1) (Table 1).

## Limitations

Stated by the authors:

- Future work only mentions non-Euclidean (hyperbolic) spaces (Conclusion); no limitation section.

Ours (assistant reading):

- Only OVEN is used, and the KG subgraph is built from OVEN's own entities (Appendix), so the setting is closed to the benchmark's entities.
- The "external knowledge" gain is not isolated in Tables 1 and 2: KnowCoL uses OpenCLIP (LAION) while CLIP2CLIP uses OpenAI CLIP, and the training recipe differs. Table 3 only removes lead images or hierarchy, not all KG knowledge.
- Training needs 4-8 H100/H200 GPUs for 22-30 hours (Appendix).
- Baseline numbers are copied from other papers (Table 1 caption).
- Relations other than P31, P279 and P171 are not ablated by type, although contribution 2 promises a study of relations.

## Relevance to the thesis

- [LIT-01](../questions/LIT-01-existing-image-sparql-benchmarks.md): contrast. Identification step only: OVEN image + intent text to a QID. No SPARQL, no multi-hop questions, no agent (Intro, Problem Definition).
- [IX-04](../questions/IX-04-index-payload.md): contrast. An entity is represented by its Wikipedia description and the mean of its lead-image embeddings (Eq. 4, 5, 12); our index stores images with a QID payload (leaning).
- [IX-03](../questions/IX-03-embedding-models.md): cite. A learned CLIP-family (OpenCLIP) embedding of entity images and text over Wikidata entities; shows fine-tuned CLIP beats vanilla CLIP on OVEN (Table 1, 2). Not comparable with our small zero-shot index.
- [AG-02](../questions/AG-02-tool-set.md): contrast. The KG is used as embeddings to train the recognizer, while our agent queries the graph with tools at inference (user's note; Eq. 12 supports that the graph is not used at inference).
- [D-008](../decisions.md#d-008) (no training): contrast. Their approach requires training on the OVEN training set (Appendix).
- [DS-12](../questions/DS-12-query-images-and-leakage.md), [DS-05](../questions/DS-05-image-role.md): possibly cite as OVEN-style query = image + intent text; not checked here.

## Citable claims

- Open-domain visual entity recognition links an image (with a text query) to an entity of a very large and evolving KG such as Wikidata, under open-set, long-tail conditions (Abstract, Intro).
- Two-step generative methods (generate a name, then BM25 over labels) lose information and suffer from semantic ambiguity when entity names are shared (Intro).
- Using Wikidata structure (type hierarchy) in training improves unseen-entity accuracy on OVEN: removing P31/P279/P171 lowers unseen accuracy from 29.1 to 25.3 for KnowCoL-L (Table 3).
- Simple fusion of the image and text query embeddings (addition) generalizes best to unseen entities; heavier fusers overfit to seen entities (Table 4).
- KnowCoL-bigG reaches 38.8 HM on the OVEN entity test split with 2.0B parameters, above Auto-VER-14B (28.9) (Table 1).

## My notes


The user's own notes. Agents never rewrite or delete this section.

- They do embeddings of the graph, while in our case the agent will have access to search the graph
- They train their models with theses embeddings? we dont do that
- They evaluate on OVEN

## Open doubts

- OVEN size: the paper says 6,063,945 "training samples" (Experiment Settings); the OVEN paper reports 6,063,945 entities. Check which is right.
- Learning rate: Training details give 0.001, the Appendix gives 0.0001 for KnowCoL-L (0.001 for H and bigG).
- Candidate set at inference: Eq. 12 takes the argmax over all entities; the size of the candidate set in their evaluation is not stated (the 32,122-entity subgraph vs the OVEN KB).
- The published AAAI version (vol. 40, 2026) may differ from arXiv v2; the text read here is arXiv v2 (18 Nov 2025).
