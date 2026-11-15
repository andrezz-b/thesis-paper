---
key: mensink2023encyclopedic
title: "Encyclopedic VQA: Visual questions about detailed properties of fine-grained categories"
authors: ["Thomas Mensink", "Jasper Uijlings", "Lluis Castrejon", "Arushi Goel", "Felipe Cadar", "Howard Zhou", "Fei Sha", "André Araujo", "Vittorio Ferrari"]
year: 2023
venue: "IEEE International Conference on Computer Vision"
url: "https://arxiv.org/abs/2306.09224"
pdf: "https://arxiv.org/pdf/2306.09224"
arxiv: "2306.09224"
doi: "10.1109/ICCV51070.2023.00289"
s2_id: "3d0eb04ca61c47161cd8eee3fb89f12da164f6e6"
code: "https://github.com/google-research/google-research/tree/master/encyclopedic_vqa"
data: "https://github.com/google-research/google-research/tree/master/encyclopedic_vqa"
status: reviewed
relevance: medium
read_depth: full
informs: [LIT-01, LIT-02, DS-01, DS-03, DS-10, AG-05]
themes: [vqa, dataset-construction, kgqa]
added: 2026-11-15
reviewed: 2026-11-15
candidates:
  - id: "arXiv:2607.21155"
    title: "CRAG-MM-Diagnostics: Enabling Stage-Wise Analysis of Knowledge-Intensive VQA"
    via: cites
    priority: high
    why: "Splits knowledge-intensive VQA into referring expression, grounding, recognition, retrieval and reasoning stages and argues end-task accuracy hides where failures occur; supports the stage-wise oracle ladder (AG-05) and metrics (EV-01, DS-13) (abstract)"
  - id: "arXiv:2404.05465"
    title: "HAMMR: HierArchical MultiModal React agents for generic VQA"
    via: cites
    priority: high
    why: "ReAct-style LLM agent with visual and knowledge tools, same group as Encyclopedic-VQA, evaluated on it including two-hop questions; design precedent for AG-02 and AG-03 (abstract and citing sentence)"
bibtex: |
  @inproceedings{mensink2023encyclopedic,
    title={Encyclopedic VQA: Visual questions about detailed properties of fine-grained categories},
    url={http://dx.doi.org/10.1109/ICCV51070.2023.00289},
    DOI={10.1109/iccv51070.2023.00289},
    booktitle={2023 IEEE/CVF International Conference on Computer Vision (ICCV)},
    publisher={IEEE},
    author={Mensink, Thomas and Uijlings, Jasper and Castrejon, Lluis and Goel, Arushi and Cadar, Felipe and Zhou, Howard and Sha, Fei and Araujo, André and Ferrari, Vittorio},
    year={2023},
    month=Oct,
    pages={3090–3101}
  }
---

# Encyclopedic VQA: Visual questions about detailed properties of fine-grained categories

## TL;DR

A large VQA dataset (221k question+answer pairs, 1M image-question-answer triplets) with questions about detailed properties of fine-grained species (iNat21) and landmarks (GLDv2). The question never names the subject (only its super category, e.g. "this monastery"). The knowledge base is free-form Wikipedia text (2M articles), not a graph, so there is no SPARQL. Closest precedent for us: question design (subject hidden, single and two-hop), oracle vs. visual-retrieval settings, and variety/disparity as diversity measures.

## Problem and contribution

- Problem: existing knowledge-based VQA sets (OK-VQA, A-OKVQA) mostly need commonsense; the few about detailed properties (S3VQA, KVQA) are small, lack attribution, or cover only celebrities (§1, Tab. 1).
- Contribution: dataset with five stated design principles: truly multimodal, encyclopedic, controlled knowledge base with answer attribution (Wikipedia section), scale, two-hop (§2). Plus experiments with PaLI, PaLM and GPT-3, with and without retrieval (§5).

## Method

Dataset construction (§4):

- Images and categories come from iNat21 (species) and GLDv2 (landmarks, from Wikimedia Commons). Only categories that map one-to-one to a Wikipedia article are used: 80% of iNat21 and 50% of GLDv2 categories (§4.1).
- Subject hidden: the question refers to the subject by its super category, so recognition is required (§4).
- Templated single-hop: experts write question templates per super category; annotators check whether the Wikipedia page answers it and mark the evidence section; unanswerable ones are dropped (§4.2).
- Automatic single-hop: a question generation model produces Q+A pairs per Wikipedia section; filtered to questions containing the category name; human annotators validate (about 80% accepted); a PaLM (FLAN) prompt rephrases the name to the super category (§4.2).
- Multi-answer: list answers, completed and verified by annotators (§4.2).
- Two-hop: the answer of a single-hop question that has its own Wikipedia page is a "bridge entity", for which a second single-hop question is generated. PaLM chains the two into one question and validates it by answering from the two single-hop QA pairs; kept only if the answer matches (§4.3).
- Each Q+A pair is paired with up to 5 images of the category (§4.4).

Evaluation: accuracy with BEM (BERT matching) at score >= 0.5, after standard VQA answer normalisation; multi-answer uses IoU >= 0.5 then BEM (§5, §5.6).

## Data / benchmark

- Is gold SPARQL released? No. No structured queries exist; the KB is free-form Wikipedia text and gold is an answer string plus the evidence section (§1, §4). Two-hop questions are chains of two text questions, not queries.
- Is the depicted entity named in the question text? No, only its super category (§4).
- Which knowledge graph? None; Wikipedia text, WIT-based, 2M English articles, snapshot of 13 August 2022 (§4.1). Wikidata is not used as KB; it appears only in related work (KAT) and Appendix C.
- Multi-hop? Single-hop (templated, automatic), multi-answer and two-hop (chained via bridge entity) (§4.2, §4.3).
- Is there an image index, and are there distractors? No index is released with the dataset; the released KB is text with images (§2, §4.1). In the Lens experiment the retrieval index is Google Lens's web-scale image index (§5.3, App. C); this is external, not part of the dataset.
- Are agentic systems evaluated? No; models get a fixed retrieved article or section in the prompt (§5.2, §5.3).
- Size, splits, licence: 1M triplets; train 1,016,251 / val 13,591 / test 5,750 triplets (Tab. 2). Test has no overlap in images with train/val; about 17% of val/test subject categories are unseen in train (§4.4). Licence: not stated in the paper text checked (code and data link: GitHub google-research repo).

Question diversity (§4.5, Tab. 3): variety = number of unique bigrams across questions (257.9k here), disparity = average cosine distance between all question pairs using Sentence-BERT (multi-qa-MiniLM-L6-cos-v1), 0.833 here.

## Key results

- No retrieval: PaLI 13.0%, PaLM 19.7%, GPT-3 15.5% (Tab. 5, single-hop).
- Oracle subject category given: PaLI 16.7%, PaLM 31.0%, GPT-3 26.9% (Tab. 5).
- Oracle KB article: 29.7% / 78.4% / 77.4%; oracle KB section: 48.8% / 87.0% / 82.1% (Tab. 5).
- Lens retrieval, KB article: 21.4% / 48.0% / 44.9%; KB section: 28.1% / 48.8% / 44.6% (Tab. 5).
- Lens finds the correct article 47.4% of the time (Tab. 6). PaLM accuracy given correct vs. incorrect retrieved section: 82.3% vs. 20.7% (Tab. 6).
- CLIP retrieval over Wikipedia title+description (as in KAT/REVIVE): recall@1 3.3%, @20 16.5%; Lens: 47.4% @1, 65.2% @20 (Tab. 7, App. C).
- Multi-answer and two-hop with Lens section retrieval: PaLI 9.2% / 14.7%, PaLM 33.6% / 22.8%, GPT-3 32.1% / 18.7% (§5.6).
- Quality: 86% of 100 sampled test questions were answerable by experts from the Wikipedia page (App. A). BEM agrees with human judgement in 96% of cases, exact match only 68% (App. B).

## Limitations

Stated by the authors:

- Two-hop questions generated by PaLM are "often incorrect" before validation, so a validation step is used (§4.3).
- The Lens retriever is a proof of concept; a specialised image classifier could substitute (App. C).

Ours (assistant reading):

- Questions are about subjects limited to species and landmarks, i.e. two domains.
- Only categories with a unique Wikipedia article are kept, so the dataset is biased towards well-documented entities.
- Models are evaluated with the retrieved text in the prompt; there is no iterative or tool-using system, so the paper says nothing about agents.
- Variety (unique bigrams) grows with dataset size, so it is not comparable to a much smaller dataset.

## Relevance to the thesis

- [LIT-01](../questions/LIT-01-existing-image-sparql-benchmarks.md): contrast. Image + question benchmark with hidden subject and two-hop questions, but Wikipedia text as KB and no SPARQL or graph (§4, Tab. 1). Cite as a precedent that is not directly reusable.
- [DS-01](../questions/DS-01-question-types.md) / [LIT-02](../questions/LIT-02-question-type-taxonomy.md): cite. Terminology: single-hop (templated, automatic), multi-answer, two-hop via "bridge entity" (§4.2, §4.3). Whether we reuse the chaining pattern for Wikidata multi-hop questions (e.g. P176 then P571) is an idea, not decided.
- [DS-03](../questions/DS-03-hop-depth.md): cite. Maximum depth in this dataset is two hops (§4.3); two-hop accuracy is lower than single-hop (§5.6).
- [AG-05](../questions/AG-05-experiment-configurations.md): adopt (partly). The ladder no retrieval / oracle subject / oracle retrieval / real retrieval (§5.1 to §5.3). Our oracle maps to "Oracle Subject C" (Tab. 5); the KB article and section oracles have no KG analogue.
- [DS-10](../questions/DS-10-dataset-size.md): cite. Disparity (§4.5) is a possible diversity measure; variety (unique bigrams) grows with dataset size and is not comparable to a small set. Not decided.
- [IX-01](../questions/IX-01-distractor-strategy.md) / [LIT-04](../questions/LIT-04-distractor-literature.md): cite only. The Lens index covers web-scale images (App. C), a point of comparison for our explicit index; the paper does not discuss distractors.
- [EV-01](../questions/EV-01-metrics.md): contrast. Accuracy via BEM (§5) vs. our execution-based comparison ([D-007](../decisions.md#d-007)); App. B shows exact match is too strict for free-text answers, which does not apply to SPARQL results.
- [DS-09](../questions/DS-09-generation-pipeline.md): cite. LLM-assisted question generation with human validation, and PaLM self-validation of chained questions (§4.2, §4.3; prompts in App. F).

## Citable claims

- Existing knowledge-based VQA sets such as OK-VQA and A-OKVQA mostly require commonsense knowledge rather than detailed properties of fine-grained entities (§1).
- A PaLI model fine-tuned for OK-VQA reaches only 13.0% accuracy on Encyclopedic-VQA single-hop questions (§5.1, Tab. 5).
- Giving the correct Wikipedia section raises PaLM to 87.0% (§5.2, Tab. 5), and retrieving the correct entity is critical: accuracy is 82.3% with a correct and 20.7% with an incorrect retrieved section (§5.4, Tab. 6).
- Two-hop questions are built by chaining single-hop questions through a bridge entity whose answer has its own knowledge-base page (§4.3).
- Questions refer to the subject only by its super category so that visual recognition is required (§4).
- Exact string matching agreed with human judgement in only 68% of cases on this dataset, BEM in 96% (App. B).
- Variety and disparity are used to compare question diversity of VQA datasets (§4.5, Tab. 3).

## My notes
- Big dataset, no SPARQL
- Again their questions can be used for examples
	- Two hop questions for harder examples, if they can be mapped in wikidata
- Variety and disparity as metrics for our dataset - or is this only applied in large datasets
	- As our dataset won't be that big, limited by the amount of gold queries we can curate
- Oracle approach
	- Subject matches entity
	- KB article/section - not applicable?
- Lens retrieval improves performance
	- Distractors builtin as it has a very large index of images

## Open doubts

- Licence of the dataset and knowledge base: not stated in the text; check the repository.
- Whether variety (unique bigrams) and disparity make sense for a few hundred items: not stated by the paper, open.
