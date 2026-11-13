---
key: loustaunau2025qawiki
title: "QAWiki: A Knowledge Graph Question Answering & SPARQL Query Generation Dataset for Wikidata"
authors: ["Alberto Moya Loustaunau", "Aidan Hogan"]
year: 2025
venue: "Wikidata Workshop 2025 (ISWC 2025), CEUR-WS Vol-4108"
url: "https://ceur-ws.org/Vol-4108/paper12.pdf"
pdf: "https://ceur-ws.org/Vol-4108/paper12.pdf"
arxiv: ""
doi: ""
s2_id: "354a417f5e8d678b19f1f75705ed2305f4a92789"
code: "https://qawiki.org/"
data: "https://doi.org/10.5281/zenodo.16787599"
status: reading
relevance: null
read_depth: null
informs: []
themes: []
added: 2026-11-08
reviewed: null
candidates:
  - id: "DOI:10.1145/3477495.3531751"
    title: "Knowledge Graph Question Answering Datasets and Their Generalizability: Are They Enough for Future Research?"
    via: refs
    priority: high
    why: "Survey of 25 KGQA datasets that QAWiki leans on for dataset quality and generalisation issues (§2); source for LIT-02 and LIT-01"
  - id: "S2:446e8de94d5b1bc91653fb58ea5de607ccf0603a"
    title: "From Transport to Grounding: Designing MCP Connectors for Reliable SPARQL Querying by LLMs"
    via: cites
    priority: medium
    scout_priority: high
    why: "Uses QAWiki as its benchmark for LLM SPARQL grounding; may inform AG-02 and AG-03 (abstract and citing sentence only)"
bibtex: |
  @inproceedings{loustaunau2025qawiki,
    title = {{QAWiki}: A Knowledge Graph Question Answering \& {SPARQL} Query Generation Dataset for {Wikidata}},
    author = {Moya Loustaunau, Alberto and Hogan, Aidan},
    booktitle = {Proceedings of the 5th Wikidata Workshop (Wikidata 2025) co-located with the 24th International Semantic Web Conference (ISWC 2025)},
    series = {CEUR Workshop Proceedings},
    volume = {4108},
    publisher = {CEUR-WS.org},
    address = {Nara, Japan},
    year = {2025},
    url = {https://ceur-ws.org/Vol-4108/paper12.pdf}
  }
---

# QAWiki: A Knowledge Graph Question Answering & SPARQL Query Generation Dataset for Wikidata

## TL;DR

QAWiki is a small (526 questions, 518 with SPARQL), handcrafted, English/Spanish KGQA and
text-to-SPARQL dataset for Wikidata, hosted on a public Wikibase (qawiki.org) with entity and
property mention annotations, quality tags and relations between questions. It evaluates GPT-4o
with SPINACH's result-table F1 and shows that giving the model the linked entities raises F1 from
0.164 to 0.406. For us it is text-only (no images), but a precedent for gold-query style, quality
tags, answer-type categories and an oracle-like "linked entities" setting.

## Problem and contribution

- Problem: most KGQA datasets are simple and single-hop, template-generated or crowdsourced with
  quality issues, English-only, and lack mention-level annotations (§1, p. 2; §2, pp. 3-4). Cites
  Jiang and Usbeck [13]: most of 25 datasets lack support for compositional / zero-shot
  generalisation; WebQuestionsSP and CWQ have factual correctness below 60% (§2, p. 4).
- Desiderata they state for KGQA datasets: (i) gold SPARQL, (ii) entity and property mention
  annotations, (iii) diverse question forms incl. paraphrases and ambiguity, (iv) multilinguality
  (§1, p. 2).
- Contribution: the QAWiki resource (§3), and an illustrative GPT-4o evaluation on QAWiki and
  SPINACH, with and without linked entities (§4).

## Method

Resource paper; the "method" is how the dataset is built and evaluated.

- Construction: almost entirely handcrafted over more than two years, mostly by the authors, some
  community contributions (§1, p. 2; §2, p. 4). LLMs (GPT-4o) suggested phrasing corrections,
  reviewed manually (§3.7, p. 9; Declaration on Generative AI). DeepSeek was used to classify
  questions (Declaration on Generative AI).
- Answer-type categories (§3.1, p. 4): entity 77, entity-set 284, numeric 45, temporal 54,
  boolean 35, miscellaneous attribute 31 (sum 526).
- Paraphrases and translations: every question in EN and ES with one or more paraphrases;
  idiomatic, not literal translation; 7 dialect variants (en-GB); community added 22 IT and 7 DA;
  3,000 question forms in total (§3.2, pp. 4-5).
- Entity and property mentions (§3.3, pp. 5-6): substrings of the question linked to QIDs/PIDs,
  annotated independently of the SPARQL query and meant to be exhaustive (alternatives included,
  e.g. "U.S. President" as Q11696, or Q30 + P35, or P1906). Property mention types: direct,
  inverse, existence, non-existence, specific value (value also given; P31/P279 excluded),
  superlative (max/min). Discontinuous mentions are captured. 5,475 mentions to 1,258 distinct
  identifiers (1,038 items, 219 properties).
- SPARQL (§3.4, pp. 6-7): each of the 518 non-ambiguous questions has one or more executable
  handcrafted queries. Criterion: write the query "as generally as possible for the question type",
  e.g. `?sbj wdt:P131*/wdt:P17?/wdt:P30? wd:Q843` for "in Pakistan", so it still works if the
  entity is replaced. Queries return Wikidata identifiers only unless the question asks for more
  (§4.1, p. 10).
- Quality tags (§3.5, p. 8). On questions: *ambiguous*, *subjective criteria*. On queries:
  *incomplete*, *no ties* (LIMIT 1 on a superlative), *controversial or unconfirmed data*. Such
  questions are kept on purpose with best-effort queries, since Wikidata cannot always give sound
  and complete answers.
- Question relations (§3.6, p. 8): *disambiguates*, *broader/narrower*, *contingent* (false
  premise check), *count of / boolean of*. The authors "believe" they could be used to test answer
  consistency, train disambiguation, and avoid false premises; the paper does not use them in any
  experiment.
- Quality control (§3.7, p. 9): 14 SPARQL queries over the Wikibase endpoint (e.g. mention not in
  question, item link not starting with "Q").
- Evaluation measure (§4.1, pp. 9-10): follows SPINACH [27]. Rows are sets of values; per-row
  recall `|g_i ∩ p_j| / |g_i|` so extra predicted columns (e.g. labels) do not hurt; Hungarian
  matching maximising total recall; F1 = 2TP / (2TP + FP + FN) with TP = sum of per-row recalls,
  FP = unmatched predicted rows, FN = unmatched gold rows and partial mismatches; EM = 1 iff F1 = 1.
- Setup (§4.2, pp. 10-11): GPT-4o, two configurations. *Base*: question only. *+Linked Entities*
  (QAWiki only): also a list of entity mentions with their Wikidata IRIs. Predicted and gold queries
  run on the live Wikidata Query Service, all in the same time frame. The prompt is not given in
  the paper.

## Data / benchmark

- Is gold SPARQL released? Yes, for all 518 non-ambiguous questions (§3.4, p. 6), CC0, snapshot
  v1 on Zenodo (§3.7, p. 9; ref. [31], DOI 10.5281/zenodo.16787599).
- Is the depicted entity named in the question text? Not applicable (text-only); entities are
  named in the question and annotated as mentions (§3.3).
- Which knowledge graph? Wikidata. Evaluation runs on the live WDQS in one time frame (§4.2,
  p. 10); no Wikidata snapshot date is stated for gold results.
- Multi-hop? Yes, mixed simple and complex questions (§1, p. 2); 2.95 predicates per query on
  average (std. 1.84) vs QALD-10 1.84, WikiWebQuestions 1.58, SPINACH 4.67 (§3.4, p. 7). Question
  types are answer-type categories (§3.1). SPARQL feature counts per dataset in Table 1 (p. 7).
- Is there an image index, and are there distractors? No (text-only).
- Are agentic systems evaluated? No; single-shot GPT-4o query generation (§4.2).
- Size, splits, licence: 526 questions (518 with SPARQL, 8 disambiguation), 3,000 question forms,
  5,475 mentions (§3.1-3.3); no splits stated, intended mainly for evaluation, also training or
  few-shot (§3.8, p. 9); CC0 (§3.7).

## Key results

- Table 2 (p. 11), GPT-4o:
  - SPINACH Base: F1 0.1887, EM 0.0836.
  - QAWiki Base: F1 0.1640, EM 0.1283.
  - QAWiki +Linked Entities: F1 0.4064, EM 0.3327.
- TP, FP and FN in Table 2 are aggregated over all queries and rows, not per question (§4.3, p. 11).
- Authors' reading (§4.3): QAWiki is harder than SPINACH in Base F1; EM is higher on QAWiki because
  it mixes simple questions and has 35 ASK queries; entity linking plays a critical role.

## Limitations

Authors say (§4.4, p. 11):
- (1) Rows are compared as sets, so a row with correct values in wrong columns counts as correct
  (also §4.1, p. 10; they believe this is rare, most queries project one column).
- (2) Live Wikidata: results may change between executions.
- (3) Result-based scoring credits a wrong query that happens to give the right result,
  especially for ASK queries.
- (4) Both datasets are on the Web and may be in GPT-4o's training data.
- Smaller than synthetic datasets (§2, p. 4).

We see (assistant reading):
- One model, one run, no prompt given; the evaluation is illustrative, not a benchmark study.
- The reported F1 does not equal 2TP / (2TP + FP + FN) computed from the aggregated totals in
  Table 2 (e.g. QAWiki Base gives about 0.04, reported 0.164), so F1 is presumably averaged per
  question; the paper does not say so.
- *+Linked Entities* gives all entity mentions with IRIs, i.e. it removes entity linking entirely,
  not only identifying one subject entity.
- Whether SPINACH's rule against zero-recall matches is used is not stated.
- 5,475 mentions in §3.3 vs 5,443 in §5.

## Relevance to the thesis

- [LIT-01](../questions/LIT-01-existing-image-sparql-benchmarks.md): contrast. Text-only Wikidata KGQA with gold SPARQL; no images, no agent (§3, §4).
- [LIT-02](../questions/LIT-02-question-type-taxonomy.md) / [DS-01](../questions/DS-01-question-types.md): cite. Six answer-type categories (entity, entity-set, numeric, temporal, boolean,
  miscellaneous attribute) with counts (§3.1, p. 4). Property mention types (direct, inverse,
  existence, non-existence, specific value, superlative; §3.3, pp. 5-6) are a second, structural
  axis.
- [DS-14](../questions/DS-14-question-labels.md): adopt ideas. Candidate label: answer-type category (§3.1). Property mention types
  (§3.3) are noted only; the user considers annotating them too costly and unlikely to be used.
  Quality tags are not labels for us (see [DS-09](../questions/DS-09-generation-pipeline.md)).
- [DS-09](../questions/DS-09-generation-pipeline.md): adopt. *Ambiguous* and *subjective criteria* (§3.5) name exactly the issues our
  acceptance criteria exclude; the user decided items with any such tag (also the query tags
  *incomplete*, *no ties*, *controversial or unconfirmed data*) are excluded rather than kept
  and tagged as QAWiki does. Quality-control queries (§3.7) and LLM phrasing review checked by a
  human (§3.7) match [D-016](../decisions.md#d-016).
- [DS-08](../questions/DS-08-gold-answers.md): adopt. Gold queries written as generally as possible with property paths (§3.4, p. 6),
  one or more gold queries per question (§3.4), gold returns identifiers only (§4.1, p. 10), and
  query tags *no ties* / *incomplete* for edge cases (§3.5); we exclude such items instead ([DS-09](../questions/DS-09-generation-pipeline.md)).
  Their general-style queries (property paths) and several gold queries per question are noted as
  options; the user is unsure about both, not adopted.
- [LIT-03](../questions/LIT-03-kgqa-metrics.md) / [EV-01](../questions/EV-01-metrics.md): adopt / cite. Confirms SPINACH's row F1 and EM (Hungarian matching, extra columns
  not penalised; §4.1); adds the limitations rows-as-sets and ASK (§4.4).
- [AG-05](../questions/AG-05-experiment-configurations.md): adopt. *+Linked Entities* (§4.2) is an oracle-like configuration; it raises F1 from 0.164 to
  0.406 (Table 2). Theirs gives QIDs for all mentions; our oracle names the entity in the text.
  The user wants a second, stronger oracle that also gives the subject's QID, next to the
  name-only one, to separate entity linking from SPARQL writing.
- [DS-04](../questions/DS-04-endpoint-snapshot.md): cite. Gold and predicted queries run on live WDQS in the same time frame (§4.2), and
  changing results are a stated limitation (§4.4).
- Thesis introduction / background: cite. §1 (pp. 1-2) introduces KGs, SPARQL, KGQA and SPARQL
  query generation with references: Hogan et al. KG survey [1], Wikidata [2], DBpedia [3], Ji et al.
  KG survey [4], QALD-9 [5], SPARQL as a Foreign Language [6], LC-QuAD 2.0 [7]; §2 surveys KGQA
  datasets (WebQSP, SimpleQuestions, LC-QuAD 1.0/2.0, QALD-7/9/10, RuBQ, MCWQ, WikiWebQuestions,
  WikidataQA, SPINACH, KQA Pro, CWQ, CFQ).

## Citable claims

- QAWiki has 526 handcrafted questions over Wikidata, 518 with SPARQL and 8 disambiguation
  questions, in English and Spanish with paraphrases (Abstract; §3.1, p. 4).
- Most KGQA datasets consist mainly of simple single-hop questions, while real queries need
  multi-hop reasoning, aggregation and temporal or comparative logic (§1, p. 2).
- KGQA performance depends heavily on accurate entity and relation linking (§1, p. 2).
- Template-generated datasets lack realism and diversity; expert curation gives smaller but
  higher-quality datasets (§2, p. 3).
- Deciding whether two SPARQL queries are equivalent is undecidable, and Wikidata's redundancy
  allows non-equivalent queries with valid answers, so they compare result tables (§4.1, p. 9).
- SPINACH's questions read like verbalisations of queries rather than questions a person would ask
  (§3.4, p. 7).
- Queries average 2.95 predicates in QAWiki vs 1.84 in QALD-10, 1.58 in WikiWebQuestions and 4.67
  in SPINACH (§3.4, p. 7).
- GPT-4o reaches F1 0.164 on QAWiki from the question alone and 0.406 when given the linked
  entities (Table 2, p. 11).
- Result-based evaluation can credit an incorrect query that returns the right results, especially
  for ASK queries (§4.4, p. 11).

## My notes
- Introduction gives a nice overview of KGs, SPARQL, KGQA, it could be used nicely in some introduction part, or a part explaining these concepts (reuse their citations)
- Broad question types to consider
- Entity and property mentions - entity mentions would actually just be the oracle setting in our case?
	- Property mentions - is this something to consider, what value does it bring
- Quality tags - issues that could complicate QA systems
	- We can discard ambiguous as we don't allow that
	- Are the others something to consider for the tagging?
- How are these question relations actually used
- Is the eval metric same as SPINACH?
- Linked entities setup matches oracle

## Open doubts

- BibTeX: DBLP blocked the script (bot check), so the `@inproceedings` entry was assembled from
  the CEUR volume page (Vol-4108, "Proceedings of the 5th Wikidata Workshop (Wikidata 2025)",
  ISWC 2025, Nara, Japan) and the paper's first page; no page range is given by CEUR. Surname is
  "Moya Loustaunau" (ref. [31] of the paper).
- How F1 in Table 2 is aggregated (per-question mean?) is not stated; see Limitations.
- Is the GPT-4o prompt or the evaluation code released? Not stated in the paper; not checked.
- Newer releases exist (search result: "QAWiki v2026.3" on Zenodo, and a WikiKGQA challenge at
  ISWC 2026 that mentions QAWiki); not checked against the v1 numbers here.
- 5,475 (§3.3) vs 5,443 (§5) annotated mentions.
