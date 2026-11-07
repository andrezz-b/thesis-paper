---
key: walter2025grasp
title: "GRASP: Generic Reasoning And SPARQL Generation across Knowledge Graphs"
authors: ["Sebastian Walter", "Hannah Bast"]
year: 2025
venue: "The Semantic Web - ISWC 2025, LNCS 16140, pp. 271-289 (2026)"
url: "https://arxiv.org/abs/2507.08107"
pdf: "https://arxiv.org/pdf/2507.08107"
arxiv: "2507.08107"
doi: "10.1007/978-3-032-09527-5_15"
s2_id: ""
code: ""
data: ""
status: reviewed
relevance: high
read_depth: full
informs: [AG-01, AG-02, AG-04, EV-01, EV-02, EV-03, DS-11]
themes: [agentic-sparql, kgqa, metrics]
added: 2026-11-06
reviewed: 2026-11-06
candidates:
  - id: "arXiv:2603.06582"
    title: "Agentic SPARQL: Evaluating SPARQL-MCP-powered Intelligent Agents on the Federated KGQA Benchmark"
    via: cites
    why: "Agentic SPARQL-tool setup with MCP tool access, evaluated on a federated KGQA benchmark; compare tool design and baselines (AG-02, EV-02) (abstract only)"
  - id: "arXiv:2512.14277"
    title: "SPARQL-LLM: Real-Time SPARQL Query Generation from Natural Language Questions"
    via: cites
    why: "Reports runtime and cost next to accuracy and classes GRASP as a toolbox-driven agent; extra metrics and baselines (EV-01, EV-02)"
  - id: "arXiv:2610.13648"
    title: "SPARQL-LLM in the TEXT2SPARQL 2026 Challenge"
    via: recs
    why: "Open-source KGQA system in a shared text-to-SPARQL challenge; possible shared benchmark and baselines (EV-02, LIT-01) (abstract only, partial)"
  - id: "S2:f5281a4defb47a4f0bc322b03a9fd3940c6ebcfc"
    title: "GRASP and GRISP for Question Answering over Wikidata"
    via: cites
    why: "Same-group follow-up on Wikidata QA; may give the latest GRASP version and Wikidata numbers (AG-01, EV-02) (title only)"
  - id: "arXiv:2210.03629"
    title: "ReAct: Synergizing Reasoning and Acting in Language Models"
    via: refs
    why: "Origin of the ReAct loop that GRASP and the thesis build on (§3.1); to cite for the agent design (AG-01, AG-03)"
bibtex: |
  @inbook{walter2025grasp,
    title={GRASP: Generic Reasoning And SPARQL Generation Across Knowledge Graphs},
    ISBN={9783032095275},
    ISSN={1611-3349},
    url={http://dx.doi.org/10.1007/978-3-032-09527-5_15},
    DOI={10.1007/978-3-032-09527-5_15},
    booktitle={The Semantic Web – ISWC 2025},
    publisher={Springer Nature Switzerland},
    author={Walter, Sebastian and Bast, Hannah},
    year={2025},
    month=Oct,
    pages={271–289}
  }
---

# GRASP: Generic Reasoning And SPARQL Generation across Knowledge Graphs

## TL;DR

GRASP lets an LLM write SPARQL for any RDF knowledge graph without fine-tuning: the model
runs a ReAct-style loop with a fixed, graph-independent set of functions (execute query,
list triples, search entities and properties via prebuilt indices). Zero-shot with
GPT-4.1 it reaches 72.5 F1 on QALD-10 and 75.3 on WWQ (Table 4). It is
the closest existing system to our agent, and SPINACH's main successor.

## Problem and contribution

- Zero-shot SPARQL QA: given a question and a SPARQL endpoint of an arbitrary RDF KG,
  produce the SPARQL query (or conclude none exists); no training data, no fine-tuning,
  but pre-computed search indices are allowed (Introduction, "Problem Formulation").
- LLMs need help with (1) finding the right IRIs and literals and (2) the finer points
  of query formulation (Introduction).
- Contributions (Introduction): first zero-shot approach that works in principle on
  arbitrary RDF KGs; evaluation on DBLP, DBpedia, Freebase, ORKG, OSM, UniProt, Wikidata;
  component studies; code, indices, benchmarks and outputs released
  (github.com/ad-freiburg/grasp).

## Method

- ReAct-like loop: interleaved reasoning and function calls, with several successive
  reasoning steps or calls allowed (§3.1). One generic instruction for all KGs, one
  continuous context from question to SPARQL (§2, §3.1).
- Functions, each with a `kg` argument (§3.2): `answer` (ANS), `cancel` (CAN),
  `execute` (EXE; shows first and last 5 rows/columns if more than 10; 60 s timeout),
  `list` triples (LST; at most 10, diverse), `search_entity` (SEN; prefix-keyword index),
  `search_property` (SPR; similarity index), `search_property_of_entity` (SPE),
  `search_object_of_property` (SOP), `search_autocomplete` (SAC), `search_constrained`
  (SCN). Search functions return the top 10. `find_similar_examples` (FSE, top 3 from
  the benchmark train set) and `find_examples` (FEX, random) are only for few-shot runs.
- Function sets (§3.3, Table 1): B (ANS, CAN, EXE), S (B + LST, SEN, SPR), S_E (S + SPE,
  SOP; default), S_C (B + LST + SCN), S_A (B + LST + SAC).
- Search indices (§3.4): built from two SPARQL queries per KG (entities, properties)
  returning IRI, label, score (popularity), synonyms, extra info (Table 2). Entities:
  prefix-keyword index. Properties: cosine similarity on mxbai-embed-large-v1
  embeddings with FAISS. Wikidata: 85M entities (12 GB data, 6 GB index), 12k properties
  (Table 3). Endpoints are QLever (§3).
- Feedback (§3.6): when the model calls ANS or CAN, the same model, seeing only the
  call's arguments and the SPARQL rules from the instruction (not the history), returns
  `done|refine|retry` plus a message; at most two intermediate feedback loops. GRASP-F
  denotes this variant.

## Data / benchmark

Not a benchmark paper. It evaluates on existing ones (WQSP, CWQ, QALD-7, QALD-10,
SPINACH, WWQ, §4.1) and builds small sets for other KGs (Table 9). No image data.

## Key results

- Metric: F1 averaged over samples, with SPINACH's modification that allows extra
  columns; 200 random samples per benchmark (full test set for QALD-7 and SPINACH)
  (§4.1).
- Zero-shot GRASP-F GPT-4.1 on Wikidata: QALD-10 70.6, QALD-7 81.5, SPINACH 42.6,
  WWQ 75.2; plain GRASP GPT-4.1: 72.5, 79.4, 40.8, 75.3. SPINACH system reported
  69.5/71.0, 74.6/72.9, 45.3/39.2, 70.3/68.3 on the same benchmarks (Table 4).
- Feedback helps zero-shot, helps less or hurts with few-shot examples (§4.2, §4.3,
  Table 8).
- Function sets (Qwen2.5 72B, Table 6): B is worst everywhere (e.g. SPINACH 17.3 vs
  27.6 for S_E); S_E best overall, S_C and S_A harder for the model to use (§4.3).
- Open models are competitive: Qwen2.5 72B reaches 68.7 on WWQ vs GPT-4.1 75.3; Qwen3 32B
  61.3 (Table 5). Reasoning models do not clearly beat non-reasoning ones (§4.3).
- Size: big jump between 7B and 14B (Qwen2.5) and between 4B and 8B (Qwen3) (Table 7).
- Few-shot: similar examples help most (Table 8).

## Limitations

Authors say (§4.4):

- The model often skips property search and hallucinates properties despite failed
  executions; returning an error for IRIs not seen in earlier results helped initially.
- Wikidata can encode the same information in different ways (single entity vs.
  property combination); the model sometimes commits to the wrong one.
- Ambiguous questions and differing `LIMIT` clauses give unfairly low F1.
- Only 200 samples per benchmark, 50 for other KGs, 100 for reasoning models (cost).

We see (assistant reading):

- Everything is text-only; no image input and no image search.
- Few-shot functions need a train set; our dataset has no train split.
- Most numbers are on 200-sample subsets with single runs; no variance reported.

## Relevance to the thesis

- [AG-01](../questions/AG-01-own-agent-vs-grasp.md): contrast / adopt. Python, open code and Wikidata support make it a possible
  base or baseline, but its generality (multi-KG `kg` argument, KG-agnostic indices) is
  out of scope ([D-003](../decisions.md#d-003)). Code link in §1 contributions.
- [AG-02](../questions/AG-02-tool-set.md): adopt. Function design to borrow from: `execute` with truncated results (§3.2),
  `list` triples, entity search, property search, property-of-entity and
  object-of-property search (S_E). Function-set study shows search tools matter and
  that simpler tools beat more flexible ones (Table 6, §4.3).
- [AG-04](../questions/AG-04-gemma-hpc.md): cite. Open models (Qwen2.5 72B, Qwen3 32B) work with GRASP; smaller ones drop
  sharply (Tables 5, 7). Relevant for the CampusAI Qwen model.
- [EV-01](../questions/EV-01-metrics.md) / [LIT-03](../questions/LIT-03-kgqa-metrics.md): adopt. Same F1 as SPINACH, extra columns allowed (§4.1).
- [EV-02](../questions/EV-02-baselines.md): cite. GRASP is a candidate text-only baseline.
- [EV-03](../questions/EV-03-ablations.md): cite. Function-set, feedback and few-shot ablations to mirror (§4.3). The
  feedback step (§3.6) is a possible ablation, not committed.
- [DS-11](../questions/DS-11-split-proportions.md): cite. Few-shot examples (FSE/FEX) need a train set; we have none ([D-008](../decisions.md#d-008)), so
  few-shot would mean taking examples from dev. Considered very unlikely.
- [IX-04](../questions/IX-04-index-payload.md): contrast. Its entity index payload is IRI, label, score, synonyms, info
  (Table 2); ours is the image index.

## Citable claims

- GRASP generates SPARQL by letting an LLM call a fixed, KG-independent set of functions
  (execute, list, search); only the endpoint changes (§1, §3.2).
- It needs no fine-tuning; pre-computed label indices are allowed (Problem Formulation).
- Compared to SPINACH, it uses one instruction and one continuous context instead of
  several subtask prompts, and its search does not rely on the Wikidata API (§2).
- Search tools are essential: with only execute, results are far worse than with search
  (Table 6, §4.3).
- A feedback step on the final answer improves zero-shot results (§4.2, Table 4).
- Open-source models can match some commercial models (§4.3, Table 5).
- Common failure: hallucinated properties instead of searching (§4.4).

## My notes
- Zero shot, uses functions for LLM to get info about knowledge graph
	- ReAct - reasoning and action, create plan, execute tools to solve problem
- Easy to make few shot - introduce functions which return examples
- Many different functions to list entities, search etc.
	- Different indexes to support this (similarity, full text)
		- What is available on wikidata?
- How do these *functions* map to SPINACH, and Wikidata, can some be simplified or combined
	- FSE and FEX if we want to use few shot, this would be an improvement only for the SPARQL generation and not really related to images
- Does Wikidata have some indexes, how are these built? Can they be used for the thesis as additional tools?
- Introduce feedback model when the original models wants to finish
	- Limit to 2 feedback loops
	- Is a feedback model something to consider?

## Open doubts

- Which Wikidata search does the thesis use: own index like GRASP, WDQS/QLever, or the
  Wikidata API as SPINACH does ([DS-04](../questions/DS-04-endpoint-snapshot.md))? Current leaning (user): the Wikidata search API
  is enough, since the thesis is Wikidata-only.
- Not checked: the released code and instruction text, and whether the Wikidata index
  can be downloaded.
