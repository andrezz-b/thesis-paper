---
key: liu2024spinach
title: "SPINACH: SPARQL-Based Information Navigation for Challenging Real-World Questions"
authors: ["Shicheng Liu", "Sina J. Semnani", "Harold Triedman", "Jialiang Xu", "Isaac Dan Zhao", "Monica S. Lam"]
year: 2024
venue: "Findings of the Association for Computational Linguistics: EMNLP 2024"
url: "https://aclanthology.org/2024.findings-emnlp.938/"
pdf: "https://aclanthology.org/2024.findings-emnlp.938.pdf"
arxiv: "2407.11417"
doi: "10.18653/v1/2024.findings-emnlp.938"
s2_id: "417966078c16c2b098ab7c842ceb3689f67ce1ec"
code: "https://github.com/stanford-oval/spinach"
data: "https://github.com/stanford-oval/spinach"
status: reviewed
relevance: core
read_depth: full
informs: [AG-02, AG-03, EV-01, LIT-03, EV-03, DS-09]
themes: [agentic-sparql, kgqa, metrics, dataset-construction]
added: 2026-11-06
reviewed: 2026-11-06
candidates:
  - id: "arXiv:2510.02200"
    title: "ARUQULA - An LLM based Text2SPARQL Approach using ReAct and Knowledge Graph Exploration Utilities"
    via: cites
    why: "Generalises SPINACH's ReAct exploration design to other RDF graphs; compare tool set and loop (AG-02, AG-03)"
  - id: "S2:354a417f5e8d678b19f1f75705ed2305f4a92789"
    title: "QAWiki: A Knowledge Graph Question Answering & SPARQL Query Generation Dataset for Wikidata"
    via: cites
    why: "Wikidata question/SPARQL dataset that compares result tables as SPINACH does (LIT-03, DS-08, DS-09)"
  - id: "arXiv:2610.06650"
    title: "Wikidata Search Traces: A Dataset for Training Knowledge Graph Search Agents"
    via: recs
    why: "Agents that explore Wikidata, with recorded search traces (AG-02, EV-03; abstract only)"
  - id: "arXiv:2604.21133"
    title: "GRISP: Guided Recurrent IRI Selection over SPARQL Skeletons"
    via: cites
    why: "Evaluates on SPINACH and WDQL with its own metric; shows how the dataset is used as a test set (LIT-03)"
  - id: "S2:f88318e3bdb5a8d39d57e2d7b48d7e3b218c2e21"
    title: "Graf von Data: A Knowledge Graph Question Answering Agent for Organisational Usage"
    via: cites
    why: "KG-agnostic ReAct agent; categorises agent actions (entity retrieval, property subgraph, path discovery, SPARQL execution) (AG-02)"
bibtex: |
  @inproceedings{liu2024spinach,
    title = {{SPINACH}: {SPARQL}-Based Information Navigation for Challenging Real-World Questions},
    author = {Liu, Shicheng and Semnani, Sina and Triedman, Harold and Xu, Jialiang and Zhao, Isaac Dan and Lam, Monica},
    editor = {Al-Onaizan, Yaser and Bansal, Mohit and Chen, Yun-Nung},
    booktitle = {Findings of the Association for Computational Linguistics: EMNLP 2024},
    month = nov,
    year = {2024},
    address = {Miami, Florida, USA},
    publisher = {Association for Computational Linguistics},
    url = {https://aclanthology.org/2024.findings-emnlp.938/},
    doi = {10.18653/v1/2024.findings-emnlp.938},
    pages = {15977--16001},
  }
---

# SPINACH: SPARQL-Based Information Navigation for Challenging Real-World Questions

## TL;DR

SPINACH contributes (a) a 320-item text-only Wikidata KBQA dataset of decontextualized
question/SPARQL pairs taken from the "Request a Query" forum, and (b) a zero-shot ReAct-style
agent that explores Wikidata with four tools and by executing partial SPARQL queries. It is the
closest published design to the thesis agent (Wikidata-specific tools, SPARQL as the output) and
the origin of the row-major F1 metric. It has no images.

## Problem and contribution

- Problem: KBQA datasets are either simple, synthetic, or use small KB schemas; systems that do
  well on them do not transfer to real queries (Abstract, §1, §2.1).
- Contributions (§1): the Spinach dataset (320 pairs, 155 dev / 165 test, §3); the Spinach agent
  (§4); a row-major generalisation of EM and F1 for multi-column answers (§5.1); new SOTA on
  QALD-7, QALD-9 Plus and QALD-10 and within 1.6 F1 of fine-tuned WikiSP on WikiWebQuestions
  (Table 2).

## Method

- Agent runs for N steps; each step outputs a thought and one action, the action is executed
  outside the agent and returns an observation (§4). State is the full history of thoughts,
  actions and observations (§4.1), not a subgraph.
- Actions (§4.1): `search_wikidata(string)` (wbsearchentities, at most 8 entities and 4
  properties returned), `get_wikidata_entry(QID)` (outgoing edges and qualifiers, pruned by a
  separate few-shot prompt, Prompt 13), `get_property_examples(PID)`, `execute_sparql(SPARQL)`
  (feedback: results, empty, syntax error text, or 60 s timeout; large results shown as first and
  last 5 rows), `stop()` (last executed SPARQL is the final answer).
- Policy (§4.2): zero-shot prompt with high-level instructions only ("start with very simple
  queries", "confirm all assumptions about Wikidata structure"; Prompt 12). Low-level control was
  tried and did not help (§4.2 Discussion). Sampling at temperature 1.0 (App. D: also nucleus
  p = 0.9), so reruns differ.
- Control: detects repeated identical actions and `stop()` after an empty result, and rolls the
  state back. Budget is 15 actions plus 15 extra for rollbacks, 30 in total (§4.2, footnote 7).
- Design differences to prior agents (§4): uses full SPARQL for exploration instead of one edge
  at a time; does not assume entities are given from the question; model is GPT-4o.

## Data / benchmark

- Is gold SPARQL released? Yes; question/SPARQL pairs, code and data at
  github.com/stanford-oval/spinach (Abstract footnote 1). Whether gold *results* are stored is
  not stated.
- Is the depicted entity named in the question text? There are no images. Entities are named in
  the text (e.g. "Leonhard Euler", Fig. 1b); annotation rules are to disambiguate entities and
  properties, and phrase naturally where this adds no ambiguity (§3.2).
- Which knowledge graph? Wikidata, queried live through the Query Service (60 s cap, §3.1, §4.1).
  A snapshot date is not stated. Forum discussions up to May 2024 were used (§3).
- Multi-hop? Question types? Not categorised. Queries are complex: 8.89 clauses, 2.50
  projections, 4.03 relations on average (Table 1). Every one of the 320 queries has a unique
  structure (Table 6). 298 unique properties (Table 7).
- Image index, distractors? None (text only).
- Are agentic systems evaluated? Yes: Spinach agent and ToG (Table 3).
- Size, splits, licence: 155 dev + 165 test (§3), no train split. Table 7 lists dataset size
  323. Dataset CC BY-SA 4.0, agent Apache 2.0 (Ethical Considerations).
- Construction (§3, App. C.3): 2780 forum discussions with a valid SPARQL; 2171 whose last query
  returns non-empty results under 10 MB; 920 randomly sampled; three expert authors annotated,
  two annotated and one cross-checked. GPT-4o suggested verbalisations and a modify/include/
  exclude decision, experts verified by running intermediate queries. `mwapi` clauses were removed
  by regex. Removed: Wikimedia presentation queries, overly complex SPARQL, optimisation clauses,
  formatting clauses (§3.1).

## Key results

- Spinach dataset, test (Table 3): Spinach agent (GPT-4o) 16.4 EM / 45.3 F1; ToG (GPT-4) 1.8 /
  7.2; fine-tuned WikiSP 1.2 / 7.1; GPT-4o writing SPARQL directly 0.6 / 3.9; GPT-4o answering
  directly 0.0 / 4.0. Dev: agent 21.4 / 46.4.
- Prior datasets (Table 2): QALD-7 74.6 F1, QALD-9 Plus 71.6 F1, QALD-10 69.5 F1 (full test),
  WikiWebQuestions test 70.3 F1 vs WikiSP 71.9.
- Ablation on dev (Table 4): full 21.4 EM / 46.4 F1; without `get_wikidata_entry` 11.7 / 36.4;
  without `get_property_examples` 10.4 / 29.4; without `search_wikidata` 4.6 / 25.3.
- Actions used (Table 5, dev): 28.6% of questions 3-5 actions, 33.8% 6-8, 19.5% hit the cap of 15.
- Cost: on average $0.1253 per question with GPT-4o (App. D.1).
- Error analysis (§5.4, 20 random cases with F1 < 0.05): 40% property problems, 30% complicated
  SPARQL, 15% not enough exploration, 10% inaccurate semantic parsing, 5% formatting.

## Limitations

Authors say:
- Multiple LLM calls per question, so latency and cost are higher than simple systems (Limitations).
- Automatic EM and F1 can misjudge LLM answers; they mitigate this by verbalising SPARQL as
  precisely as possible (Limitations).
- Annotation errors are possible; mitigated by cross-validation among experts (Limitations).
- The dataset is small; dev set can only separate systems at least 9.0% apart (C.2).

We see (assistant reading):
- The Wikidata state is live; no snapshot is given, so reproducing gold results later may differ.
- Baselines were made easier than their normal setting (gold entities for WikiSP, up to 20 gold
  result entities as ToG topic entities, §5.3), but the Spinach agent gets no entities. The ToG
  re-implementation used live API calls rather than a local index (App. D).
- Error analysis is only 20 cases of failures.
- Only GPT-4o is evaluated as the agent model; no open model is tested.

## Relevance to the thesis

- [AG-02](../questions/AG-02-tool-set.md): adopt. The four Wikidata tools plus `stop` (§4.1) are the starting point for the
  thesis tool set; image-index search is added as one more tool in the same loop. The ablation
  (Table 4) shows every tool matters, `search_wikidata` most.
- [AG-03](../questions/AG-03-agent-framework.md): adopt. The high-level zero-shot policy prompt (§4.2, Prompt 12) is the starting point
  for the agent prompt.
- [AG-01](../questions/AG-01-own-agent-vs-grasp.md): cite / contrast. SPINACH is the design the own agent would follow; code is released
  (Apache 2.0). Whether to build on it is for [AG-01](../questions/AG-01-own-agent-vs-grasp.md) to decide.
- [EV-01](../questions/EV-01-metrics.md) and [LIT-03](../questions/LIT-03-kgqa-metrics.md): adopt. Row-major EM and F1 that do not penalise extra columns (§5.1), computed
  with an optimal row assignment (SciPy `linear_sum_assignment`). Note that baselines that return
  labels were compared on labels (App. D).
- [EV-03](../questions/EV-03-ablations.md): adopt. Remove one tool at a time (§5.5); error categories from §5.4 as a template.
- [DS-09](../questions/DS-09-generation-pipeline.md): cite. LLM-assisted construction with expert verification is established practice here,
  which supports [D-016](../decisions.md#d-016): GPT-4o proposes verbalisations and a modify/include/exclude decision,
  experts verify by executing queries (App. C.3). Mention this in the thesis method section.
- [DS-08](../questions/DS-08-gold-answers.md) and [DS-04](../questions/DS-04-endpoint-snapshot.md): cite. Gold results are queries run on live WDQS filtered for non-empty results
  under 10 MB, with optimisation and formatting clauses removed (§3, §3.1); QLever on the latest
  dump failed for them (App. D).
- [DS-10](../questions/DS-10-dataset-size.md): cite. 320 items, 155 dev and 165 test, with the minimum-detectable-effect argument for
  why this is enough (App. C.2).
- [LIT-02](../questions/LIT-02-question-type-taxonomy.md), [DS-13](../questions/DS-13-difficulty-levels.md) and [DS-14](../questions/DS-14-question-labels.md): cite. Table 1 characterises complexity by counting SPARQL features
  (definitions in App. A); Table 6 counts unique query patterns (App. B). Possible source of
  difficulty labels.
- [LIT-01](../questions/LIT-01-existing-image-sparql-benchmarks.md): contrast. Text-only; it contains no image input.

## Citable claims

- Existing KBQA datasets are simple, synthetic, or based on small schemas, and results on
  synthetic datasets overestimate real-world performance (§1, §2.1).
- Subgraph-state agents cannot answer questions with many answer entities or needing computation
  (§4).
- An agent can write SPARQL by mixing exploration with query writing, using the full history as
  state (§4, §4.1).
- High-level policy instructions worked better than low-level control of the action choice (§4.2).
- LLM suggestions followed by expert verification can be used to build a KBQA dataset
  (App. C.3).
- Each of the search, entry and property-example actions contributes to accuracy (Table 4).
- Row-major F1 is defined to not penalise additional projection columns (§5.1).
- The dataset's 320 queries all have unique query patterns (Table 6) and 298 unique properties
  (Table 7).
- The agent beats ToG and WikiSP on the Spinach dataset by a wide margin (Table 3), yet reaches
  only 45.3 F1 on test, which the authors read as room for improvement (§5.3).
- Dominant failure modes are wrong property use and complicated SPARQL (§5.4).

## My notes

- Wikidata question and SPARQL dataset generated from real forum questions
	- Further cleaned up by the authors
- Is the quantitative analysis in table 1 relevant in any way
- I think the dataset part can be ignored
### Agent
- Builds from simpler queries to the result query
- Try many queries and fail early
- What does this mean
- Zero shot - agent has tools to explore the wikidata relevant to the task
- Formalization of exploration state, actions and outputs could be useful for the writing part
- Tools used - `search_wikidata`, `get_wikidata_entry`, `get_property_examples`, `execute_sparql`
- Limiting results, and pruning wikidata entry with separate agent
- High level policy encouraging exploration, with a limit on actions
### Evaluation
- Row major EM and F1 which do not penalize extra columns
- Error analysis - something useful to have in my paper
- Ablation study with removing tools

## Open doubts

- Whether gold results are stored with the dataset, and which Wikidata snapshot was used, are
  not stated.
- Only GPT-4o is tested as the agent model. Whether the zero-shot high-level prompt also works
  with a weaker open model (CampusAI, [AG-04](../questions/AG-04-gemma-hpc.md)) is unknown.
