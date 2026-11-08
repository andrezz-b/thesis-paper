---
key: hu2023open
title: "Open-domain Visual Entity Recognition: Towards Recognizing Millions of Wikipedia Entities"
authors: ["Hexiang Hu", "Yi Luan", "Yang Chen", "Urvashi Khandelwal", "Mandar Joshi", "Kenton Lee", "Kristina Toutanova", "Ming-Wei Chang"]
year: 2023
venue: "IEEE/CVF International Conference on Computer Vision (ICCV)"
url: "https://arxiv.org/abs/2302.11154"
pdf: "https://arxiv.org/pdf/2302.11154"
arxiv: "2302.11154"
doi: "10.1109/ICCV51070.2023.01108"
s2_id: ""
code: ""
data: ""
status: reviewed
relevance: medium
read_depth: full
informs: [LIT-01, LIT-04, IX-01, IX-02, IX-03, IX-04, DS-09, DS-13, DS-14, EV-03]
themes: [vqa, dataset-construction, distractors]
added: 2026-11-08
reviewed: 2026-11-08
candidates:
  - id: "arXiv:2510.13675"
    title: "Seeing and Knowing in the Wild: Open-domain Visual Entity Recognition with Large-scale Knowledge Graphs via Contrastive Learning"
    via: cites
    priority: very high
    why: "2025 open-domain visual entity recognition linking images to Wikidata-style large KGs with contrastive learning; direct comparison for the identification step, LIT-01, IX-01 and IX-03 (abstract only)"
  - id: "arXiv:2403.02041"
    title: "A Generative Approach for Wikipedia-Scale Visual Entity Recognition"
    via: cites
    priority: high
    why: "Successor to OVEN on the same 6M-entity space, comparing generative and dual-encoder recognition; LIT-04 and IX-02 for how candidate-set size affects accuracy (abstract and citing sentences)"
  - id: "arXiv:2410.23676"
    title: "Web-Scale Visual Entity Recognition: An LLM-Driven Data Approach"
    via: cites
    priority: high
    why: "Uses an LLM for label verification, metadata and rationale when building visual entity recognition data; a model for DS-09 given the LLM-assisted, manually curated pipeline (D-016) (abstract only)"
bibtex: |
  @inproceedings{hu2023open,
    title={Open-domain Visual Entity Recognition: Towards Recognizing Millions of Wikipedia Entities},
    url={http://dx.doi.org/10.1109/ICCV51070.2023.01108},
    DOI={10.1109/iccv51070.2023.01108},
    booktitle={2023 IEEE/CVF International Conference on Computer Vision (ICCV)},
    publisher={IEEE},
    author={Hu, Hexiang and Luan, Yi and Chen, Yang and Khandelwal, Urvashi and Joshi, Mandar and Lee, Kenton and Toutanova, Kristina and Chang, Ming-Wei},
    year={2023},
    month=Oct,
    pages={12031--12041}
  }
---

# Open-domain Visual Entity Recognition: Towards Recognizing Millions of Wikipedia Entities

## TL;DR

OVEN defines the task of linking an image plus a short text query (which states only the
recognition intent, not the entity) to one of about 6M English Wikipedia entities, and
OVEN-Wiki is a benchmark built by re-purposing 14 recognition and VQA datasets. It is the
"identify the depicted entity" step of our pipeline as a stand-alone benchmark, without any
downstream question answering or SPARQL. Useful to us for how the unnamed-entity query is
written, the head/tail analysis, the effect of candidate-set size and the error analysis.

## Problem and contribution

- Existing recognition benchmarks fix the label granularity or domain, and VQA datasets focus
  on high-level categories (§1). OVEN uses Wikipedia as one universal label space with
  flexible granularity (§1, §2).
- Task: input is an image and a text query that expresses the intent; output is the linked
  Wikipedia entity (§2). Only entities physically present in the image are in scope; entities
  that are not shown (e.g. the inventor of the airplane) are deferred to follow-up work
  (footnote 4, §2), which is InfoSeek (see `chen2023can`).
- Contributions: the task, the OVEN-Wiki dataset (§3), and a study of fine-tuned CLIP-based
  retrieval and PaLI-based generation models (§4 to §6).

## Method

- Knowledge base: triples of (entity, text, set of images). Only the entity name is used as
  text, and only the first infobox image of the Wikipedia page as visual support; entities
  without one get a black image (§2 footnote 2, §3, §5.1).
- Dual encoders (retrieval): CLIP ViT-L14 vanilla, CLIP Fusion (two-layer multimodal
  transformer on top of CLIP features), CLIP2CLIP (cosine similarities of image/text pairs
  between query and entity, combined by four learnable weights). ScaNN is used for search
  over 6M candidates (§4.1).
- Encoder-decoder (generation): PaLI 3B and 17B fine-tuned to generate the entity name, which
  is mapped to a Wikipedia entity with BM25 over names (§4.2).
- Images are resized to 224x224 and normalised as in each model's pre-training (§5.1).

## Data / benchmark

- Is gold SPARQL released? No. The gold label is a Wikipedia entity (§2, §3); there is no
  query language or answer beyond the entity.
- Is the depicted entity named in the question text? No, by design: the query only states
  the intent ("What is the model of the car?"). For the human set annotators rewrote queries
  so that no other object can be the answer, and so that the answer is not contained in the
  question (§1, Appendix 10.2 item 3).
- Which knowledge graph? English Wikipedia dump of 2022-10-01, 6,063,945 entities after
  removing disambiguation, redirect and media pages (§3, Fig. 3 right). Wikidata is used
  only to mine the super-category for source datasets that lack one (Appendix 10.1). Example
  entity IDs in the paper are Wikidata QIDs (§2, e.g. Q7395937).
- Multi-hop? No; single-step recognition (§2). Query templates are generated from the
  super-category ("what is the species of the plant in this image?", Appendix 10.1).
- Image index and distractors? Infobox images exist for 2,032,340 of the 6,063,945 entities
  (§3). Every other KB entity is effectively a distractor, there is no curated distractor
  set. The candidate-size study sub-samples negatives (how is not stated) (§6, Fig. 5).
- Agentic systems evaluated? No (§4).
- Size, splits, licence: train 4,958,569 / val 129,490 / test 729,259 / human 24,867
  examples; seen vs unseen entities (Fig. 3 mid). Licence of the data is not stated in the
  paper; it is released at open-vision-language.github.io/oven (footnote on p. 1).
- Super-categories (Fig. 3 left): animal 19.4%, plant 16.0%, building 13.8%, location 5.8%,
  food 4.1%, person 4.0%, organization 3.8%, others 33.0%.

## Key results

- Test, overall harmonic mean (Table 2): PaLI-17B 20.2, PaLI-3B 11.8, CLIP2CLIP 5.3,
  CLIP Fusion 4.1, CLIP 2.4. On the human set: PaLI-17B 31.6, CLIP2CLIP 12.4.
- Human with search engines: 77.7 harmonic mean on 100 sampled examples, 3 annotators,
  about 254 s per example (§5.2, Table 2 and footnote 7).
- Candidate-set size (Fig. 5, §6): CLIP2CLIP accuracy drops roughly linearly in log
  candidate count from 20K to 6M; PaLI is flatter.
- Head vs tail (Fig. 6, §6): PaLI is better on entities with more than 5K monthly
  Wikipedia page views; CLIP2CLIP is on par or better below 2.5K.
- Error analysis (Table 3, §6; 100 random human-set examples): PaLI-17B 29% correct, errors
  mostly "wrong but relevant" 23%, "too generic" 15%, "misunderstand query" 7%,
  miscellaneous 24%. CLIP2CLIP 15% correct, "misunderstand query" 37%.
- Appendix 10.2: on the human set annotators flagged 8.4% of entity links as wrong and
  10.3% of answers as not physically present; 99.9% of queries were rewritten.

## Limitations

Stated by the authors:

- Only entities visible in the image are covered; extension to non-visible entities is left
  to follow-up work (§2 footnote 4).
- PaLI is not constrained to the KB, so it relies on BM25 post-processing; constrained
  decoding is left for the future (§6).
- Models trained longer lose accuracy on unseen entities (Fig. 4, §6).

We see (assistant reading):

- Single-step recognition only; nothing about reasoning over a knowledge graph.
- The label space is Wikipedia, not Wikidata, and only infobox images are used, so
  coverage of Wikidata P18 images is not addressed.
- The human-eval protocol (rewritten queries, three annotators) is described, but no
  agreement numbers are given in what we read.

## Relevance to the thesis

- [LIT-01](../questions/LIT-01-existing-image-sparql-benchmarks.md): contrast. OVEN is the closest standalone benchmark for the identification step
  (image + intent query, entity not named), but its output is an entity, with no gold SPARQL
  or KG question answering (§2, footnote 4 defers that to InfoSeek).
- [LIT-04](../questions/LIT-04-distractor-literature.md) / [IX-01](../questions/IX-01-distractor-strategy.md) / [IX-02](../questions/IX-02-distractor-count.md): cite. Distractors are the full KB; Fig. 5 shows recognition
  accuracy falls with candidate-set size, which supports varying the number of distractors.
- [IX-03](../questions/IX-03-embedding-models.md): cite. Vanilla CLIP ViT-L14 is weak as a retriever on 6M entities (Table 1, 2),
  and CLIP-style retrieval is relatively better on tail entities (Fig. 6). We use CLIP
  ViT-B/32 in the POC.
- [IX-04](../questions/IX-04-index-payload.md): cite. Entity text for retrieval is the name only and the visual support is the
  first infobox image (§2 footnote 2, §3).
- [DS-13](../questions/DS-13-difficulty-levels.md) / [DS-14](../questions/DS-14-question-labels.md): possible adopt. Head vs tail (by monthly page views, Fig. 6) as a
  difficulty or label axis.
- [DS-02](../questions/DS-02-wikidata-subset.md): cite. Super-category distribution (Fig. 3 left) as a reference for how skewed a
  Wikipedia-derived entity set is.
- [DS-09](../questions/DS-09-generation-pipeline.md): adopt (idea). Human annotation to remove ambiguity: rewrite the query so no other
  object is a valid answer and the entity is not leaked (Appendix 10.2).
- [EV-01](../questions/EV-01-metrics.md): cite. Human performance with search tools as a reference point (§5.2).

## Citable claims

- "Linking an image to one of about 6M English Wikipedia entities, with a text query stating
  only the recognition intent, is the OVEN task." (§1, §2)
- "OVEN-Wiki is built from 14 existing recognition, retrieval and VQA datasets, with labels
  grounded to Wikipedia entities." (§3)
- "Fine-tuned PaLI-17B outperforms CLIP-based retrieval overall (test hm 20.2 vs 5.3 for
  CLIP2CLIP), but CLIP2CLIP is on par or better on tail entities (<2.5K monthly views)."
  (Table 2, Fig. 6, §6)
- "Retrieval accuracy of CLIP2CLIP decreases as the number of candidate entities grows from
  20K to 6M." (Fig. 5, §6)
- "Humans with search engines reach 77.7% harmonic mean accuracy, far above the best model."
  (§5.2, Table 2; 100 examples)
- "Human annotators rewrote the queries so that no other object in the image could be a valid
  answer." (§3, Appendix 10.2)

## My notes
- Using human annotation to avoid ambiguous answers
- Distribution of super categories - perhaps connected to my question about well connected parts of Wikidata (although unsure how much Wikidata == Wikipedia)
- Pretraining not relevant
- Data processing - do we need to consider specific formats for our vision model or the embedding model
- Tail and head entities based on wikipedia page visits
- Is error analysis something that we could include in the thesis, it would be small sample but maybe a nice thing to write a little bit about

## Open doubts

- Fig. 3 (left) gives "others" as 33.0% and Appendix Fig. 8 gives 25.5%; the two groupings
  are not reconciled in the text.
- How negatives are sub-sampled in Fig. 5 is not stated.
- Whether a query image can coincide with the entity's infobox image (leakage, [DS-12](../questions/DS-12-query-images-and-leakage.md)) is not
  stated in what we read.
- Data licence is not stated in the paper; check the project page before reusing data.
