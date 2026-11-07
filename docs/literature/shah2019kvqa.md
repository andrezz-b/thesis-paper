---
key: shah2019kvqa
title: "KVQA: Knowledge-Aware Visual Question Answering"
authors: ["Sanket Shah", "Anand Mishra", "Naganand Yadati", "P. Talukdar"]
year: 2019
venue: "AAAI Conference on Artificial Intelligence"
url: "https://doi.org/10.1609/aaai.v33i01.33018876"
pdf: "https://doi.org/10.1609/aaai.v33i01.33018876"
arxiv: ""
doi: "10.1609/aaai.v33i01.33018876"
s2_id: "d0818dac77eee5b970736e57a478bcedfb1b15fe"
code: ""
data: "http://malllabiisc.github.io/resources/kvqa/"
status: reviewed
relevance: medium
read_depth: full
informs: [LIT-01, LIT-02, LIT-04, DS-01, DS-04, DS-05, DS-13, DS-14, IX-01, AG-05]
themes: [dataset-construction, kgqa, distractors]
added: 2026-11-06
reviewed: 2026-11-07
candidates:
  - id: "DOI:10.1145/3591106.3592227"
    title: "Explicit Knowledge Integration for Knowledge-Aware Visual Question Answering about Named Entities"
    via: cites
    priority: low
    why: "Explicit KB integration for KVQAE, an extension of the KVQA task; LIT-01, AG-05 (abstract only)"
  - id: "arXiv:2604.05818"
    title: "WikiSeeker: Rethinking the Role of Vision-Language Models in Knowledge-Based Visual Question Answering"
    via: cites
    priority: medium
    why: "2026 KB-VQA multimodal RAG using the image as retrieval key; IX-01, AG-05 (abstract only)"
  - id: "arXiv:2306.00424"
    title: "End-to-end Knowledge Retrieval with Multi-modal Queries"
    via: cites
    priority: medium
    why: "Retrieval with image+text queries; reference for index search; IX-01, LIT-04 (abstract only)"
bibtex: |
  @article{shah2019kvqa,
    title={KVQA: Knowledge-Aware Visual Question Answering},
    volume={33},
    ISSN={2159-5399},
    url={http://dx.doi.org/10.1609/aaai.v33i01.33018876},
    DOI={10.1609/aaai.v33i01.33018876},
    number={01},
    journal={Proceedings of the AAAI Conference on Artificial Intelligence},
    publisher={Association for the Advancement of Artificial Intelligence (AAAI)},
    author={Shah, Sanket and Mishra, Anand and Yadati, Naganand and Talukdar, Partha Pratim},
    year={2019},
    month=July,
    pages={8876–8884}
  }
---

# KVQA: Knowledge-Aware Visual Question Answering

## TL;DR

Early dataset (183K QA pairs, 24,602 images, 18,880 persons) for VQA that needs world knowledge about *named* entities, here only persons depicted in Wikipedia images, answered over Wikidata with multi-entity, multi-relation and multi-hop reasoning (Table 2, §KVQA). Gold answers come from hand-written SPARQL templates, but the queries are deliberately not released (S3). For us it is an early example of Wikidata-grounded questions with a visual entity-linking step, a question-challenge taxonomy and an open-world setting with many distractor identities. It has no agent, no released SPARQL and only person entities.

## Problem and contribution

- Problem: conventional and commonsense VQA (KB-VQA, FVQA) concern common nouns; questions about named entities in the image need world knowledge (Intro, Fig. 1).
- Contributions (Intro): (1) defines knowledge-aware VQA (KVQA); (2) the KVQA dataset, claimed to be the first for this task and "more than 12x larger" than commonsense-VQA datasets; (3) baselines for visual entity linking and for QA.
- Also provides a support set of reference images for 69K persons from Wikidata for visual named entity linking (Intro, §Knowledge Graph).

## Method

Dataset construction (§Data collection and annotation):
- S1: list of athletes, politicians and actors from Wikidata; about 30K persons, about 70K images and captions harvested from their Wikipedia pages.
- S2: human annotators prune images with no or too many persons and exact duplicates, then label who is in the image, their left-to-right order and their Wikipedia pages (captions as an aid).
- S3: annotators write templated questions; the authors write SPARQL queries over Wikidata for the ground-truth answers. Templates and SPARQL are "only used to obtain ground truth, and are not provided along with the questions".
- S4: splits, five random splits provided; accuracy is to be averaged over them.
- S5: test questions are paraphrased with an online tool, and humans accept, refine or discard each suggestion.

Baselines (§Approach): visual entity linking as face identification (face detection by Zhang et al. 2016, FaceNet 1-nearest-neighbour against reference images, MS-Captionbot as comparison); QA with a 3-layer memory network over KG facts (up to 3 hops) plus spatial facts (face coordinates), BLSTM as alternative.

## Data / benchmark

- Is gold SPARQL released? No. SPARQL is used only to obtain ground-truth answers (S3); released are question-answer-image tuples (and preprocessed KG facts, reference images per the project page, not checked in the paper).
- Is the depicted entity named in the question text? Mixed: questions refer to people by position or description ("person second from left", "the two people in the image", "Who among the people ... eldest?"), but some name one person in the image ("Who is to the left of Hillary Clinton?") (Fig. 2). No systematic statement about this.
- Which knowledge graph? Wikidata, RDF dump of 2018-05-05 (a fixed snapshot); 5.2K relations, 12.8M entities, 52.3M facts; subset for 114K persons (§Knowledge Graph).
- Multi-hop? Yes, up to 3 hops. Closed world: 18 pre-specified relations (e.g. occupation, country of citizenship, place of birth); open world: 200 most frequent relations (§Knowledge Graph, p. 8881). Ten, non-exclusive challenge categories: spatial, 1-hop, multi-hop, Boolean, intersection, subtraction, comparison, counting, multi-entity, multi-relation (§Analysis of KVQA, Fig. 2). Question-category counts are not given.
- Image index and distractors? Support set with one reference image per person: 18K entities (closed world) or 69K entities (open world) (§Knowledge Graph, §Approach). The 69K identities act as distractors; the authors attribute the closed-to-open drop partly to "a large number of distractors" (§Approach, p. 8883). No hard-negative selection.
- Agentic systems evaluated? No. Memory network and BLSTM baselines, trained end-to-end on the train split (§Approach).
- Size, splits, licence: 183,007 QA pairs, 24,602 images, 18,880 unique entities, 19,571 unique answers, 7.44 questions per image (Table 2). Splits about 17K/5K/2K images and about 130K/34K/19K QA pairs, five splits (S4). Licence: not stated in the paper.

## Key results

- Visual entity linking (Table 3): FaceNet closed world top-1 precision 81.0, recall 82.2; open world 73.5 and 71.4. MS-Captionbot precision 95.2, recall 16.6.
- QA (Table 4), original questions, no captions: closed-world MemNet 49.5, BLSTM 47.2; open-world MemNet 36.0, BLSTM 16.8. With paraphrased test questions: closed-world MemNet 32.0, open-world 26.2. Oracle (faces solved) closed-world MemNet 59.2.
- Per category, oracle, original questions, MemNet (Table 5): Boolean 75.1, intersection 72.5, 1-hop 61.0, multi-hop 53.2, comparison 50.5, counting 49.5, spatial 48.1, multi-relation 45.2, multi-entity 43.5, subtraction 40.5.
- Paraphrasing costs about 17 points for MemNet in the closed world without captions (49.5 to 32.0, Table 4), but only about 1 point per category in the oracle ablation (Table 5), so the drop comes from the full pipeline rather than from reasoning alone (assistant reading; not discussed by the authors).

## Limitations

Authors say (§Discussion): limited to persons, other entity types (monuments, events) left to future versions; off-the-shelf face descriptors fall short with many distractors; memory networks do not scale to many facts.

We see (assistant reading):
- Only person entities identified by face, so the "image entity" is a face-recognition problem; not transferable to objects such as products.
- Model baselines are old (2019 memory network), no LLM or agent.
- Table 4 caption refers to the "Visual Entity Linking" section for an oracle explanation, which is described in the text under VQA over KG.
- Text of S4 says 70/20/10 "for train, test, and validation", while the sizes (17K, 5K, 2K) suggest train/validation/test; order is inconsistent.
- No released SPARQL, so queries cannot serve as our gold-query reference.

## Relevance to the thesis

Proposed, pending your agreement:

- [LIT-01](../questions/LIT-01-existing-image-sparql-benchmarks.md): contrast. Wikidata-based, multi-hop, image plus question, but gold SPARQL is withheld on purpose (S3) and the entity is a face; no agent. Our gold SPARQL and non-person entities are the difference.
- [LIT-02](../questions/LIT-02-question-type-taxonomy.md): cite / adopt for terminology. Ten non-exclusive challenge categories (§Analysis of KVQA, Fig. 2, Table 5).
- [DS-14](../questions/DS-14-question-labels.md): adopt the idea. Non-exclusive tags per question, as in your note "tagging in my case".
- [DS-01](../questions/DS-01-question-types.md): cite. Templates written by annotators and instantiated with SPARQL over Wikidata (S3), analogue of M3-VQA's templates.
- [LIT-04](../questions/LIT-04-distractor-literature.md) / [IX-01](../questions/IX-01-distractor-strategy.md): cite. Open-world index of 69K identities as the distractor set, with measured performance drop (Table 4, §Approach); distractors are simply all other entities, not chosen by similarity.
- [AG-05](../questions/AG-05-experiment-configurations.md): cite. Oracle setting where entity recognition is assumed solved (§Approach, Table 4), the same idea as our oracle configuration.
- [DS-13](../questions/DS-13-difficulty-levels.md): cite. Per-category difficulty (Table 5) and closed vs open world as a difficulty knob.
- [DS-04](../questions/DS-04-endpoint-snapshot.md): cite. Fixed Wikidata RDF dump (2018-05-05) as snapshot (§Knowledge Graph).
- [DS-05](../questions/DS-05-image-role.md): cite. Images with several people and spatial questions (Fig. 2) vs our single-subject image.

## Citable claims

- KVQA contains 183,007 QA pairs about 18,880 unique entities in 24,602 images (Table 2).
- The authors state KVQA is the only dataset in their comparison that needs world knowledge about named entities in the image (Table 1, §Related Work).
- Answers were obtained by SPARQL queries over Wikidata from annotator-written question templates; the queries are not released (S3, p. 8879).
- Test questions were paraphrased to make the task more realistic, with human acceptance of each suggestion (S5).
- Questions are grouped into ten non-exclusive challenge categories (§Analysis of KVQA).
- Memory-network accuracy falls by more than 10 points when moving from the closed to the open world; the authors attribute it to visual entity linking errors with many distractors and to fact selection from a large fact set (§Approach, p. 8883).
- With face recognition assumed solved, the memory network handles 1-hop, Boolean and intersection questions best and spatial, multi-hop, multi-relation, subtraction, counting and multi-entity questions worst (Table 5, p. 8883).

## My notes

- Big dataset focusing on named entities (persons) from wikidata
- Multi relation, multi entity, multi hop
	- Like M3 we could use some of their datapoints for inspiration, perhaps even more so because they built on wikidata (How much of this is already present in M3)
- Question classification - multi-entity, intersection, boolean, subtraction, spatial...
	- Tagging in my case
- Is paraphrasing something to consider, or too much?
- SPARQL only used for dataset generation?

## Open doubts

- Is the depicted person ever named in a question outside the examples in Fig. 2? Not stated.
- Split order (train/test/validation vs train/validation/test) is inconsistent in S4.
- No numbers per question category and no template count are given; the released dataset.json might tell, not checked.
- Licence of the data and reference images: not stated in the paper, not checked on the project page.
- How well does the 2018 Wikidata dump still match current Wikidata? Not checked.
