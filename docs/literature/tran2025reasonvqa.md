---
key: tran2025reasonvqa
title: "ReasonVQA: A Multi-hop Reasoning Benchmark with Structural Knowledge for Visual Question Answering"
authors: ["Duong T. Tran", "Trung-Kien Tran", "Manfred Hauswirth", "Danh Le Phuoc"]
year: 2025
venue: "IEEE/CVF International Conference on Computer Vision (ICCV) 2025"
url: "https://arxiv.org/abs/2507.16403"
pdf: "https://arxiv.org/pdf/2507.16403"
arxiv: "2507.16403"
doi: "10.1109/ICCV51701.2025.01746"
s2_id: ""
code: "https://github.com/duong-tr/ReasonVQA"
data: "https://reasonvqa.duongtr.com"
status: reviewed
relevance: high
read_depth: full
informs: [LIT-01, DS-09, DS-13, DS-14, EV-01]
themes: [kgqa, dataset-construction, vqa]
added: 2026-11-06
reviewed: 2026-11-07
candidates:
  - id: "arXiv:2511.22843"
    title: "Breaking the Visual Shortcuts in Multimodal Knowledge-Based Visual Question Answering"
    via: cites
    why: "KB-VQA benchmark where the query image no longer matches the subject entity; related-entity images; LIT-04, IX-01, DS-07, DS-12 (abstract only)"
  - id: "arXiv:2609.20843"
    title: "VISPATH: Visual-Intent-Guided Path Reasoning for Multimodal Knowledge Graph Question Answering"
    via: cites
    why: "Multimodal KGQA with KG-path reasoning and a 2 to 4 hop benchmark; LIT-01, AG-03 (abstract only)"
  - id: "arXiv:2602.00593"
    title: "Pix2Fact: When Vision Is Not Enough -- Benchmarking Fine-Grained VQA with Web Verification on High-Resolution Real-World Scenes"
    via: cites
    why: "Benchmark needing visual grounding plus external search, evaluated with search tools; LIT-01 contrast, EV-02 (abstract only)"
  - id: "DOI:10.1109/CVPR.2019.00686"
    title: "GQA: A New Dataset for Real-World Visual Reasoning and Compositional Question Answering"
    via: refs
    why: "Template engine over Visual Genome scene graphs with answer balancing that ReasonVQA reuses; DS-09, DS-13, DS-14 (via Semantic Scholar refs only)"
  - id: "arXiv:1602.07332"
    title: "Visual Genome: Connecting Language and Vision Using Crowdsourced Dense Image Annotations"
    via: refs
    why: "Objects, relations, scene graphs and WordNet synsets; ReasonVQA's image source; LIT-05, DS-12 (abstract only)"
bibtex: |
  @misc{tran2025reasonvqa,
    doi = {10.48550/ARXIV.2507.16403},
    url = {https://arxiv.org/abs/2507.16403},
    author = {Tran, Duong T. and Tran, Trung-Kien and Hauswirth, Manfred and Phuoc, Danh Le},
    keywords = {Computer Vision and Pattern Recognition (cs.CV), FOS: Computer and information sciences, FOS: Computer and information sciences},
    title = {ReasonVQA: A Multi-hop Reasoning Benchmark with Structural Knowledge for Visual Question Answering},
    publisher = {arXiv},
    year = {2025},
    copyright = {arXiv.org perpetual, non-exclusive license}
  }
---

# ReasonVQA: A Multi-hop Reasoning Benchmark with Structural Knowledge for Visual Question Answering

## TL;DR

ReasonVQA is a template-based pipeline plus a large VQA benchmark (4.2M questions, 598K images) whose
questions need Wikidata facts, with 1 to 3 hops. Questions refer to the depicted object by class
("this church"). Wikidata is queried via SPARQL to link objects and fetch facts, but the released items are
question + answer (open-ended or 4-way multiple choice), not gold SPARQL. Closest existing work to our dataset
idea on the generation side; it differs in task (VQA answers, not SPARQL), in having no image index, and in
evaluating only plain VLMs without tools.

## Problem and contribution

- Problem: knowledge-based VQA datasets are small or need much human effort (OK-VQA, KVQA, InfoSeek,
  Encyclopedic-VQA), or use only commonsense (CRIC) or synthetic scenes (LORA) (§1, §2).
- Contributions: (1) a benchmark of multi-hop questions needing external knowledge, (2) a low-cost, scalable
  generation framework, (3) evaluation of 13 VLMs (§1).

## Method

- Image sources: Visual Genome (VG, objects with scene graphs) and Google Landmarks v2 (GLDv2) (§3.1).
- Linking (App. 1.2): VG objects carry WordNet synset names, converted with NLTK to a synset ID and looked up in
  Wikidata by SPARQL. GLDv2 landmarks: the name is extracted heuristically from the Wikimedia URL and searched in
  Wikidata.
- Facts are collected as triples from the root concept, up to three hops (App. 1.2).
- Questions: manually written templates, one main template per Wikidata property and an optional sub-clause
  template; 182 main templates, 100 sub-clause templates, 182 properties (App. 1.2). A k-hop question nests the
  sub-clause templates, e.g. "Who designed this skyscraper?" -> "...the architect of ..." (§3.2.1, Fig. 4).
  Scene graph relations can be used as sub-clauses ("__ parked next to the sidewalk").
- The placeholder is filled with the class name of the main object ("instance of"/"subclass of"). The answer is
  obtained in the same retrieval of facts (§3.2.1).
- Multiple choice: up to N=3 false choices, generated per answer category (fixed set, date within +-10 years,
  number in a range, literal from the same property) (§3.2.2).
- Balancing of the answer distribution per property (top ten answers, GQA-inspired) gives ReasonVQA-B (§3.3.1).
  Split 70/30 train/test by image, no image overlap (§3.3.2).
- 20 predefined domains; questions are tagged by the property used (§3.2.1, App. 2.2).

## Data / benchmark

- Is gold SPARQL released? Not stated in the paper. SPARQL is used for linking and fact retrieval (§3.1,
  App. 1.2); the question representation is a template composition, not a query. Project page
  (https://reasonvqa.web.app) and demo (https://reasonvqa.duongtr.com): no mention of SPARQL; the demo shows
  question, answer choices and hop count and has a Download page (content not checked). The code repository
  (https://github.com/duong-tr/ReasonVQA) contained only a LICENSE file with one commit when checked
  (2026-11-07), although the paper says source code is provided (§5).
  The data is on Hugging Face (`duongtr/ReasonVQA`, checked 2026-11-07 via the Download page, a Hugging Face
  API call and range reads of the files). Per question there is an annotation record with `hop`, `entity_id` (QID
  of the main entity), `entity_name`, `route` (list of QIDs from the main entity to the answer node),
  `property_id` and `property_label` (PID of the last property only) and `has_scene_graph`. Still no SPARQL. The
  intermediate properties of a multi-hop route are not stored; example: question 171 has hop 2, route
  Q11746980 -> Q179718 -> Q2886278 and property P2348 (time period), while the first property (P138, named after)
  is only visible in the 1-hop question 169 about the same entity.
- Is the depicted entity named in the question text? No (also in the released data, e.g. "After whom or what is
  this church named?"), the class name is used ("this church", "this skyscraper")
  (§3.2.1, Fig. 1). For GLDv2 landmarks the main object is a specific entity; for VG the linked concept is a
  WordNet-derived Wikidata concept (e.g. traffic light, App. 1.2, Fig. 1).
- Which knowledge graph? Wikidata. Snapshot or endpoint: not stated.
- Multi-hop? Yes, 1/2/3 hops (full: 1.36M / 2.81M / 5.4K; ReasonVQA-U: 23.8K / 49.5K / 4.8K; App. 2.1 Table 2).
  Question types are by property (what/who/how tall...), no taxonomy such as comparison, count or yes/no stated.
- Image index and distractors? None. The images are the input; for multiple choice, distractors are answer
  choices, not images (§3.2.2).
- Agentic systems? No. Only VLMs prompted zero-shot and three fine-tuned (§4.2).
- Size: full 598.5K images, 4.2M questions; ReasonVQA-U 13.3K images, 78K questions; ReasonVQA-B 8.7K images,
  51.9K questions (§4.1 Table 1). Splits: 70/30 train/test (§3.3.2). Licence: not stated in the paper; the Hugging Face dataset card says `agpl-3.0`, the project page and demo say "This work is licensed under AGPL 3.0" and the repository has an AGPL-3.0 LICENSE (2026-11-07). The licences of the source images (VG, GLDv2) are not discussed in the paper.

## Key results

- Zero-shot open-ended, semantic-similarity accuracy on ReasonVQA-U: GPT-4o 62.8, Qwen2.5-VL 59.3, Idefics2 50.8,
  mPLUG-Owl2 22.1 (Table 2, top block). Multiple choice: GPT-4o 76.6, Mantis-Idefics2 68.7 (Table 2, bottom block).
- Scores are lower than on VQAv2 and OK-VQA, e.g. Qwen2.5-VL 59.3 vs 84.9 on OK-VQA (Table 2).
- Balanced version slightly lower than unbalanced (Table 2, §4.4).
- 3-hop is clearly harder; 1-hop only slightly better than 2-hop, in some cases worse (§4.4, Fig. 6).
  Scene-graph questions score lower than others (§4.4).
- Exact match scores low because models give free text ("very high" vs "390 meters"); semantic similarity
  (all-MiniLM-L6-v2) is used as main metric (§4.3, §4.4).
- Fine-tuning with LoRA on the train split: Qwen2-VL-7B 59.0 -> 65.0, PaliGemma-2-3B-Mix 40.1 -> 66.8,
  PaliGemma-2-10B-Mix 65.6 -> 74.5 (Table 3).
- User study, 1000 question-image pairs, 20 participants: 96% of answers correct; 83.9% of questions rated
  natural or very natural (58.1% + 25.8%); 2.5% with grammar errors (§4.1).

## Limitations

Stated by the authors:

- Naturalness has "room for improvement" (§4.1). Numeric answers (e.g. city area) and height/length ambiguities
  are the main source of wrong answers (§4.1).
- Number of hops is capped at three to limit grammatical errors (App. 1.2).

We see (assistant reading):

- Only 5.4K of the 4.2M questions are 3-hop; only 4.8K in ReasonVQA-U (App. 2.1 Table 2).
- Evaluation is by string or semantic similarity of the answer text, not by comparing query results.
  Semantic similarity can reward near misses on numbers or dates.
- Multiple choice distractors are random draws (dates +-10 years, number ranges), so MC is easy to
  guess by plausibility; the open-ended setting is the more informative one.
- Only 13 plain VLMs are evaluated: no retrieval, no tools, no agents, so nothing is said about how the
  external knowledge could be accessed.
- For VG, the linked entity is a class concept; the answers then come from class-level facts, which may be
  generic (not checked in examples).

## Relevance to the thesis

Proposed, to be confirmed with the user (no `relevance`/`informs` set yet).

- [LIT-01](../questions/LIT-01-existing-image-sparql-benchmarks.md): contrast. Wikidata, image-based, 1 to 3 hops, but no gold SPARQL, no image index, no agent (§3, §4.2;
  Data checklist).
- [DS-09](../questions/DS-09-generation-pipeline.md): cite. Template-per-property generation with nested sub-clauses is the query-first alternative to our
  LLM-assisted, manually curated pipeline ([D-016](../decisions.md#d-016)); it still produces no gold SPARQL, so we do not adopt it. Note
  it if we ever move away from LLM curation (§3.2.1, App. 1.2). The user study is a possible quality check (§4.1).
  The user's idea of reusing its items as a starting point is recorded in [DS-09](../questions/DS-09-generation-pipeline.md); the released annotations (QID, route, last
  property; see Data section) make it feasible for GLDv2 items.
- [LIT-05](../questions/LIT-05-visual-knowledge-graphs.md) / [DS-05](../questions/DS-05-image-role.md) / [DS-13](../questions/DS-13-difficulty-levels.md): cite. Scene-graph (VG) relations as extra sub-clauses add visual context and
  lower scores (§3.2.1, §4.4), a possible route to the "more complex images" idea.
- [DS-12](../questions/DS-12-query-images-and-leakage.md): cite/adopt idea. VG and GLDv2 as image sources with Wikidata links (§3.1); GLDv2 URLs point to
  Wikimedia Commons.
- [DS-13](../questions/DS-13-difficulty-levels.md) / [DS-14](../questions/DS-14-question-labels.md): adopt. Hop count as difficulty label (Fig. 6, §4.4).
- [DS-03](../questions/DS-03-hop-depth.md): cite. Up to 3 hops chosen as trade-off with grammatical errors (App. 1.2).
- [DS-01](../questions/DS-01-question-types.md): contrast. Question types follow properties; no comparison, count or boolean types.
- [EV-01](../questions/EV-01-metrics.md) / [LIT-03](../questions/LIT-03-kgqa-metrics.md): contrast. Their metric (exact, substring, semantic similarity) is answer-text based, ours is
  execution-based (§4.3).
- [AG-05](../questions/AG-05-experiment-configurations.md) / [EV-02](../questions/EV-02-baselines.md): cite. Baselines are VLMs with image + question only (§4.2); this is the "vision only" setting
  without tools.

## Citable claims

- Wikidata is the knowledge base; the framework is said to be adaptable to other knowledge bases and annotated
  vision datasets (§3.1, §5).
- Questions have 1, 2 or 3 hops, built by nesting manually written templates per property (§3.2.1).
- The largest version has about 598K images and 4.2M questions, stated to be one to two orders of magnitude
  larger than similar knowledge-based VQA datasets (§1, §4.1 Table 1).
- Zero-shot, most VLMs do clearly worse on ReasonVQA than on VQAv2 and OK-VQA (§4.4, Table 2).
- Accuracy drops for 3-hop questions compared with 1-hop and 2-hop (§4.4, Fig. 6).
- 96% of the sampled questions had a correct answer in a user study with 20 participants and 1000 pairs
  (§4.1).
- The released data (Hugging Face, project Download page) gives per question the main-entity QID, a route of QIDs and
  the last property, not SPARQL (project page; checked 2026-11-07, not in the paper).
- Existing knowledge-based datasets such as InfoSeek and Encyclopedic-VQA needed human annotation or validation
  (§2, authors' characterisation).

## My notes
- Dataset generation method
	- Is it only multiple choice?
- SPARQL only used to get the ground truth, no gold query
- VG has scene graph annotations - could be useful for finding images that we can then use in our examples
- Could we instead of having multiple choice, just convert the correct answer to a SPARQL query (if possible)
- In the evaluation, what do the models get as input, image and question? how do they access the external knowledge?

## Open doubts

- Released annotations contain the main-entity QID, the route of QIDs and the last property, but not the
  intermediate properties; a gold SPARQL would have to be reconstructed (checked on a few rows only). The
  repository had no code on 2026-11-07 (only LICENSE), contrary to §5.
- Sample of 6,671 rows at ten offsets of `val.jsonl`: all from GLDv2, none from Visual Genome (not a full
  count). The data is therefore mostly landmark and building images; check the share of Visual Genome questions.
- Multiple-choice distractors in the released rows look implausible (e.g. country of a church: Malawi,
  Vanuatu, Kosovo for the answer Poland; time period: May, November). The released rows hold `answers` and
  `correct` per question.
- `image_url` points to Wikimedia Commons for GLDv2 images (per-file licences not checked); `image_path` is
  empty in the rows read.
- Dataset download: the demo has a Download page; format, contents and licence of the data itself are not checked.
- The repository had no code on 2026-11-07 (only LICENSE), contrary to §5.
- The BibTeX in the front matter is the arXiv `@misc`; the paper is ICCV 2025 (DOI 10.1109/ICCV51701.2025.01746).
  Replace it when the thesis cites the paper.
- How are VG questions about class concepts (e.g. "traffic light") answerable at the instance level? Check
  examples in Fig. 6 and the dataset.
- Only the arXiv v3 HTML and the project/demo pages were read; page numbers not given.
