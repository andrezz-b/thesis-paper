---
key: chen2023can
title: "Can Pre-trained Vision and Language Models Answer Visual Information-Seeking Questions?"
authors: ["Yang Chen", "Hexiang Hu", "Yi Luan", "Haitian Sun", "Soravit Changpinyo", "Alan Ritter", "Ming-Wei Chang"]
year: 2023
venue: "EMNLP 2023"
url: "https://arxiv.org/abs/2302.11713"
pdf: "https://arxiv.org/pdf/2302.11713"
arxiv: "2302.11713"
doi: "10.18653/v1/2023.emnlp-main.925"
s2_id: ""
code: ""
data: ""
status: reviewed
relevance: high
read_depth: full
informs: [LIT-01, LIT-02, DS-01, DS-08, DS-09, DS-13, IX-01, IX-03, IX-04, LIT-04, AG-05, EV-01, EV-02]
themes: [vqa, kgqa, dataset-construction, distractors]
added: 2026-11-06
reviewed: 2026-11-08
candidates:
  - id: "arXiv:2302.11154"
    title: "Open-domain Visual Entity Recognition: Towards Recognizing Millions of Wikipedia Entities"
    via: refs
    priority: very high
    why: "OVEN: the entity recognition task, 100K Wikipedia KB and CLIP2CLIP model behind InfoSeek's With-KB protocol; bears on LIT-04, IX-01 and IX-03 (not read; known from InfoSeek §4.2)"
  - id: "arXiv:2306.09224"
    title: "Encyclopedic VQA: Visual questions about detailed properties of fine-grained categories"
    via: refs
    priority: high
    why: "Concurrent Wikipedia-entity VQA benchmark with a KB (InfoSeek §6 calls it concurrent work); LIT-01 landscape, possibly two-hop questions for LIT-02 and DS-03 (not verified)"
  - id: "arXiv:2407.12735"
    title: "EchoSight: Advancing Visual-Language Models with Wiki Knowledge"
    via: cites
    priority: medium
    scout_priority: high
    why: "Image-to-Wikipedia retrieval plus LLM answering, evaluated on InfoSeek and EVQA; retrieval baseline for IX-03 and EV-02, but we do not train (abstract and citing sentences)"
  - id: "arXiv:2607.00159"
    title: "Identifying and Resolving Pitfalls of Knowledge-Based VQA Benchmarks: Auditing, Repairing, and Augmenting"
    via: cites
    priority: high
    why: "Audits KB-VQA benchmarks including InfoSeek for answer-validity assumptions behind accuracy metrics; bears on EV-01, DS-08 and LIT-01 (abstract)"
  - id: "DOI:10.18653/v1/2024.emnlp-main.613"
    title: "Large Language Models Know What is Key Visual Entity: An LLM-assisted Multimodal Retrieval for VQA"
    via: cites
    priority: high
    scout_priority: medium
    why: "An LLM names the key visual entity before retrieval, close to our agent's grounding step; AG-05 and IX-03 (abstract)"
bibtex: |
  @inproceedings{chen2023can,
    title = "Can Pre-trained Vision and Language Models Answer Visual Information-Seeking Questions?",
    author = "Chen, Yang  and Hu, Hexiang  and Luan, Yi  and Sun, Haitian  and Changpinyo, Soravit  and Ritter, Alan  and Chang, Ming-Wei",
    editor = "Bouamor, Houda  and Pino, Juan  and Bali, Kalika",
    booktitle = "Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing",
    month = dec,
    year = "2023",
    address = "Singapore",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.emnlp-main.925/",
    doi = "10.18653/v1/2023.emnlp-main.925",
    pages = "14948--14968",
  }
---

# Can Pre-trained Vision and Language Models Answer Visual Information-Seeking Questions?

## TL;DR

InfoSeek is a visual QA dataset of questions about a depicted Wikipedia/Wikidata entity whose answers are not in the image or in common knowledge. It has a human-written split (8.9K) and a large template-generated split from Wikidata triples (1.3M). The paper also defines two protocols: No-KB (end-to-end VQA models) and With-KB (CLIP entity recognition over a 100K Wikipedia KB, then text QA), and shows that entity recognition is the bottleneck (Oracle entity: about 20% to about 50%). For us it is the closest precedent for "image + question that does not name the entity + Wikidata-derived answer", but it has no SPARQL and no agent.

## Problem and contribution

- Problem: existing knowledge-based VQA benchmarks do not test fine-grained, information-seeking questions. 70.8% of 500 sampled OK-VQA questions can be answered without a search engine (§2, Fig. 1, App. C.1); a question-only PaLM reaches 31.5% on ViQuAE, above the SOTA retrieval model (§2, Table 1); K-VQA covers only persons (§2).
- Contribution: the InfoSeek dataset (§3), the No-KB / With-KB protocols (§4), and a baseline study of PaLI, PaLI-X, BLIP2, InstructBLIP and CLIP-based pipelines (§5).
- Built on OVEN (Hu et al. 2023) entity annotations (§2, §3).

## Method

- **InfoSeek_Human** (§3.1, App. A.1): annotators see entity images, a 15-word description and Wikipedia section titles, and write 3-5 questions per entity; a second group labels answers as a short span from the Wikipedia article and the type (Time, Numerical, String). Rules reject binary questions, visual attributes and questions that copy the entity name. Expert check: 95% of 200 sampled answers correct (Table 8).
- **InfoSeek_Wikidata** (§3.2, App. A.2): Wikidata triples (snapshot 2022-10-03) for 300 selected relations are turned into questions with one or two human-written templates per relation. The template has a placeholder for a hypernym of the entity (e.g. "car") and for units. Images are paired with the QA pairs. Filtering keeps a QA pair only if the answer is found in the entity's Wikipedia article (exact or fuzzy match; time +/- 1 year). Subsampling balances (relation, category) pairs and answers per relation, following RoMQA.
- **Splits** (§3.3): Unseen Question and Unseen Entity; overall score is their harmonic mean. Train, Val, Test and Human sizes: Table 7.
- **No-KB protocol** (§4.1): end-to-end models fine-tuned on InfoSeek_Wikidata (PaLI-17B, PaLI-X, BLIP2, InstructBLIP), plus Random, Prior and a question-only PaLM 540B baseline (5-shot).
- **With-KB protocol** (§4.2): (1) visual entity recognition: CLIP ViT-L/14, fine-tuned as CLIP2CLIP from OVEN; the query is the (image, question) pair, the candidates are (Wikipedia image, Wikipedia title) pairs from a 100K KB; top k=5 by weighted cosine similarity. (2) Text QA: PaLM 5-shot with "This is {entity} {question}", or FiD (T5-large) reading 100 passages from the 5 retrieved entities. The KB holds the InfoSeek visual entities plus top frequent Wikipedia entities (§4). Oracle: gold entity instead of retrieval.

## Data / benchmark

- Is gold SPARQL released? Not stated. QA pairs come from Wikidata triples and templates, but no query is described or released in the paper.
- Is the depicted entity named in the question text? No. Templates use a hypernym placeholder (§3.2); in the Human split, questions that reveal the entity name are rejected (App. A.1).
- Which knowledge graph? Wikidata snapshot 2022-10-03 for the generated split (§3.2); answers are checked against Wikipedia (App. A.2). The human split uses Wikipedia answers only (§3.1).
- Multi-hop? Not stated; each question comes from one triple (subj, relation, obj) (§3.2), so we (and the user) read it as single-hop. Question types are answer types: Time, Numerical, String (§3.1, Table 7).
- Image index and distractors? A 100K Wikipedia KB (articles and infobox images) with the visual entities of InfoSeek and top frequent Wikipedia entities (§4). No hard-negative selection is described. Images for questions come from 9 classification/retrieval datasets (App. A.4: ImageNet21k-P, iNaturalist2017, Cars196, SUN397, Food101, Sports100, Aircraft, Oxford Flower, Google Landmarks v2).
- Agentic systems evaluated? No; pipelines and end-to-end models only.
- Size, splits, licence: Wikidata 1.35M IQA triples, 11,481 entities, 2,739 entity types; Human 8.9K, 806 entities (Table 2). Train 934,048 / Val 73,620 / Test 347,980 / Human 8,931 (Table 7). Licence of the dataset: not stated in the paper. Data page: https://open-vision-language.github.io/infoseek/ (footnote 1).

## Key results

- No-KB, overall (Table 4): PaLI-X 22.1 (Wikidata) / 10.8 (Human); PaLI-17B 18.1 / 8.2; BLIP2 13.9 / 9.4; InstructBLIP 13.7 / 9.9; PaLM question-only 4.3 / 5.6; Prior 3.2 / 0.3.
- Same models on OK-VQA: PaLI-X 66.1 (Table 4), a large gap to InfoSeek.
- With-KB (Table 5): CLIP to PaLM 20.1 / 15.2; CLIP to FiD 19.3 / 18.2; Oracle to FiD 52.0 / 45.6. Entity recognition accuracy of CLIP is 22.2 (the table row is ambiguous about which pipeline it belongs to).
- Zero-shot vs fine-tuned (Fig. 3): PaLI zero-shot is negligible, fine-tuning raises it; InstructBLIP zero-shot 7.4 vs BLIP2 11.3 on Wikidata, because of coarser answers (§5.1).
- Question types (Table 6, unseen question split): No-KB models are weak on Time (3.8 to 7.9) and Numerical; With-KB CLIP to PaLM gets 12.5 Time and 27.7 Numerical.
- Head vs tail entities (Fig. 7, §5.2): PaLI-17B beats the pipelines on tail entities (low page views), pipelines win on popular entities.
- Real-world test (§5.1): 90 questions on 30 author-taken images; PaLI-17B 22.2%, PaLI-X 38.9%.

## Limitations

Authors say (§8): English only; knowledge from Wikipedia only; other domains and updates to Wikipedia are future work.

We see (assistant reading):
- Answers are checked against Wikipedia text, not against Wikidata at query time; the filter removes questions where Wikidata and Wikipedia disagree (App. A.2).
- Template questions are single-relation; the dataset does not test multi-hop reasoning or query generation.
- Entity recognition uses a fine-tuned CLIP2CLIP model, so the retrieval numbers are not comparable to zero-shot retrieval.
- Models are large Google-internal ones (PaLM 540B, PaLI-X 55B); results are not reproducible by us.

## Relevance to the thesis

- [LIT-01](../questions/LIT-01-existing-image-sparql-benchmarks.md): contrast. Image plus entity-free question with Wikidata-derived answers, but no gold SPARQL, single triple per question, no agent (§3.2, §4).
- [LIT-02](../questions/LIT-02-question-type-taxonomy.md) / [DS-01](../questions/DS-01-question-types.md): cite. Question types are answer types (Time, Numerical, String), not structural types (§3.1, Table 6).
- [DS-09](../questions/DS-09-generation-pipeline.md): adopt ideas. Human-written templates per Wikidata relation with a hypernym placeholder (§3.2), filtering for answer consistency, and relation-category subsampling to avoid skew (App. A.2). Same template approach as M3-VQA (see my notes).
- [IX-01](../questions/IX-01-distractor-strategy.md) / [LIT-04](../questions/LIT-04-distractor-literature.md): adopt as an additional strategy. The With-KB KB mixes the benchmark entities with top frequent Wikipedia entities (§4); we could add a pool of general entities next to the same-class distractors.
- [IX-03](../questions/IX-03-embedding-models.md) / [IX-04](../questions/IX-04-index-payload.md): contrast. Query is a multimodal (image, question) embedding against (Wikipedia image, Wikipedia title) candidates, top-5 (§4.2); our index is image-only, QID payload.
- [AG-05](../questions/AG-05-experiment-configurations.md) / [EV-02](../questions/EV-02-baselines.md): adopt. Question-only baseline (§4.1) and Oracle entity upper bound (Table 5) match our planned oracle and no-image configurations.
- [DS-13](../questions/DS-13-difficulty-levels.md): cite. Entity popularity (monthly page views) changes which approach wins (Fig. 7); candidate difficulty axis (user agrees). For the vision-only configuration (no index), more popular entities should be recognised better, so popularity is also worth logging as a label ([DS-14](../questions/DS-14-question-labels.md)). Answer type also shifts difficulty (Table 6).
- [DS-08](../questions/DS-08-gold-answers.md) / [EV-01](../questions/EV-01-metrics.md): cite. Answer matching with Wikidata aliases (avg 4.5), +/- 1 year for time, 10% range tolerance for numbers (App. A.3). We use execution-based comparison instead. Their Wikipedia-consistency filter (97% of answers found, App. A.2) is worth listing explicitly as a check, though for us the Wikidata entity itself holds the answer.

## Citable claims

- Existing knowledge-based VQA sets such as OK-VQA mostly need only common knowledge: 70.8% of 500 sampled questions could be answered without a search engine (§2, App. C.1).
- Questions in ViQuAE can often be answered without the image: question-only PaLM scores 31.5% (§2, Table 1).
- InfoSeek has a human-written split (8.9K) and a template-generated Wikidata split (1.3M) (§3, Table 2).
- The generated questions use human-written templates for 300 Wikidata relations; answers were kept only if found in the entity's Wikipedia article (§3.2, App. A.2).
- Fine-tuned end-to-end models stay low on InfoSeek (best overall 22.1 on Wikidata, 10.8 on Human) while reaching 66.1 on OK-VQA (Table 4).
- A pipeline of visual entity recognition and text QA outperforms end-to-end models on the human split (Table 5, §5.2).
- Replacing CLIP entity recognition with oracle entities raises accuracy from about 20% to about 50% (§5.2, Table 5).
- End-to-end models are better on tail entities, pipelines on popular ones (Fig. 7, §5.2).

## My notes
- Wikidata part of infoseek can be used as inspiration for my data
- Templating approach similar to M3
- During the With-KB protocol they provide Wikipedia articles for entities from InfoSeek and other frequent entities - their distractor strategy perhaps we can adopt it as having a pool of general entities in addition to the negative distractors or other strategies
- Question only baseline
- Mutlimodal embeddings - (image, question) to query (wiki image, wiki title) from KB
- Oracle

## Open doubts

- Venue and BibTeX: the user supplied the ACL Anthology entry (EMNLP 2023, pp. 14948-14968); it replaces the arXiv `@misc` and uses the note key. The abstract field was left out.
- No licence for the data is stated in the paper; check the data page.
- Whether the released data includes the Wikidata relation/property IDs per question (this would help us map their relations to our hop paths) is not checked.
- Which pipeline the 22.2 entity accuracy in Table 5 belongs to is unclear from the table layout.
