---
key: walter2026grisp
title: "GRISP: Guided Recurrent IRI Selection over SPARQL Skeletons"
authors: ["Sebastian Walter", "Hannah Bast"]
year: 2026
venue: "arXiv.org"
url: "https://arxiv.org/abs/2604.21133"
pdf: ""
arxiv: "2604.21133"
doi: "10.48550/arXiv.2604.21133"
s2_id: "3198b9387391f97ea5d813bd1dd398525408e01c"
code: "https://github.com/ad-freiburg/grasp"
data: ""
status: reviewed
relevance: low
read_depth: full
informs: [AG-01, LIT-03, EV-02, AG-02]
themes: [kgqa, fine-tuning, wikidata]
added: 2026-11-15
reviewed: 2026-11-15
candidates:
  - id: "arXiv:2610.08095"
    title: "Natural Language Questions as an Interface for Knowledge Graphs: QRAKEN Graph Distillation and Semantic Self-Healing"
    via: recs
    priority: medium
    why: "Training-free, ontology-agnostic text-to-SPARQL that grounds generation in populated graph patterns and repairs queries; possible idea for an agent exploration tool (AG-02). (abstract seen)"
  - id: "S2:6a48700bd6d8d1ab5fa4b882c5cb8b692a3055d7"
    title: "Structured Agentic Retrieval over Knowledge Graphs with MCP and Query Containers"
    via: recs
    priority: medium
    why: "Agentic KG retrieval exposed through MCP tools; comparison point for tool-set design (AG-02). (title only)"
bibtex: |
  @misc{walter2026grisp,
    doi = {10.48550/ARXIV.2604.21133},
    url = {https://arxiv.org/abs/2604.21133},
    author = {Walter, Sebastian and Bast, Hannah},
    keywords = {Computation and Language (cs.CL), FOS: Computer and information sciences},
    title = {GRISP: Guided Recurrent IRI Selection over SPARQL Skeletons},
    publisher = {arXiv},
    year = {2026},
    copyright = {arXiv.org perpetual, non-exclusive license}
  }
---

# GRISP: Guided Recurrent IRI Selection over SPARQL Skeletons

## TL;DR

GRISP is a fine-tuned small language model (Qwen2.5 7B) that answers questions over a
knowledge graph in two stages: it generates SPARQL skeletons with natural-language
placeholders, then resolves the placeholders left to right with retrieve-and-re-rank under
KG constraints and backtracking. It beats other fine-tuning methods (ChatKBQA, WikiSP) and is
much faster than the agentic GRASP, but needs question-query training pairs and loses to
GRASP with GPT-4.1 when training data is scarce (QALD-7, QALD-10, SPINACH).

## Problem and contribution

- Problem: agentic zero-shot KGQA (GRASP, SPINACH) is slow and needs large, expensive models;
  existing fine-tuning methods (ChatKBQA, WikiSP) are tied to one KG or benchmark (§1, §2).
- Contribution: a KG-agnostic generate-then-retrieve method whose novelty is the placeholder
  resolution stage (backtracking search, retrieve-and-re-rank, KG constraints) (§1, Core
  Contributions). Code is part of the GRASP repository; checkpoints, benchmarks and
  predictions are released (§1).

## Method

- Stage 1 (§3): beam search (width 8, with sampling) over the SLM produces SPARQL skeletons
  where every IRI is a `PH:"label"` placeholder. Duplicates and unparsable skeletons are
  dropped; the top 3 go on.
- Stage 2 (§3): placeholders are resolved left to right. For each, the entity or property
  index (from GRASP) is searched with the label; the top 10 alternatives plus a *None*
  alternative are re-ranked list-wise by the same SLM in one forward pass (single-token
  identifiers, as in FIRST). Alternatives ranked above *None* are kept on a stack.
- KG guidance (§3): triple patterns of the already resolved prefix are turned into a
  single-column SPARQL query; the index search is restricted to the returned IRIs. Skipped
  inside constructs such as UNION.
- Backtracking (§1, §3): if *None* ranks first, constrained retrieval is empty, or the
  final query fails to execute or returns nothing, GRISP goes back one step, drops the
  failed alternative and re-ranks the rest. When a skeleton is exhausted it moves to the next
  one and returns the first valid result.
- Training (§4): one SLM trained jointly on skeleton generation and re-ranking, with data
  synthesised from question-query pairs (placeholders from label or alias; augmentations:
  random top-k, dropped metadata, dropped target, shuffling). LoRA r=32, 4 epochs.

## Data / benchmark

Not a dataset paper. It evaluates on existing benchmarks: CWQ, WQSP (Freebase); QALD-7, WWQ,
SPINACH, WDQL, QALD-10, LC-QuAD 2.0, SimpleQuestions, QAWiki (Wikidata) (§4). All are text
only; there are no images.

## Key results

- F1 with Qwen2.5 7B (Table 1): CWQ 75.1, WQSP 76.0, QALD-7 47.8, WWQ 79.5, WWQdev 85.3,
  SPINACH 29.35, WDQL 57.6 (random 1000-sample subset, trained on WDQL). Time per question
  2.3 s to 14 s (Tables 1, 2).
- Versus GRASP (Table 3): GRASP GPT-4.1 reaches 44.5 / 52.3 / 75.3 on CWQ / WQSP / WWQ against
  GRISP 77.0 / 73.3 / 78.8, but 79.8 / 72.7 / 40.8 on QALD-7 / QALD-10 / SPINACH against
  GRISP 46.7 / 44.5 / 29.3. GRASP needs 17 to 136 s per question, GRISP 3.7 to 14 s.
  Note the SPINACH number for GRISP is from a model trained on WDQL (Table 3, footnote).
- Ablation on WWQdev (Table 5): F1 84.4 full; removing re-ranking 78.6, beam search 79.0,
  KG guidance 80.7, constrained search 83.2, backtracking 83.9; all mechanisms off 70.4.
- Oracle skeleton (§4, failure modes): WWQdev F1 98.6 vs 84.4; QALD-10 94.6 vs 46.5, so
  skeleton generation is the main bottleneck.
- Model size (Table 4c): 0.5B 74.8, 1.5B 80.8, 3B 81.6, 7B 85.3 F1 on WWQdev.

## Limitations

- Authors say (Limitations): needs question-query training pairs; falls behind agentic
  methods in low-data regimes and on harder, diverse queries (QALD-7, QALD-10, SPINACH);
  single training run per configuration; results may be wrong and are not to be trusted
  blindly. It stops at the first non-empty result, with no plausibility check (§5).
- We see: SPINACH has no train split, so GRISP is trained on WDQL there, which is not
  directly comparable to zero-shot agents. The paper's own authors also develop GRASP,
  so the comparison is within one group (assistant reading).

## Relevance to the thesis

- [AG-01](../questions/AG-01-own-agent-vs-grasp.md): cite. Same group and same repository as GRASP (§1); shows the GRASP code base is
  being extended, but GRISP itself is a trained system.
- [AG-02](../questions/AG-02-tool-set.md): adopt (idea only). GRISP's KG-constrained search (list only properties that occur
  for the already resolved entity, §1, §3) could become an agent tool, e.g. "properties
  of this entity", so the agent sees only valid options. Only the idea carries over; GRISP
  uses a trained re-ranker, the agent would pick itself. Not decided (assistant reading).
- [LIT-03](../questions/LIT-03-kgqa-metrics.md): cite. Uses row-wise F1 averaged over samples plus Exact Match, following GRASP (§4,
  Metric).
- [EV-02](../questions/EV-02-baselines.md): cite. Needs training pairs, which the thesis dataset will not have ([D-008](../decisions.md#d-008)), so it is
  not a usable baseline. Its Table 3 is useful context on how fine-tuned and agentic
  methods compare.

## Citable claims

- Agentic zero-shot KGQA systems such as GRASP and SPINACH are slow and rely on large,
  expensive models (§1).
- With enough question-query training pairs, a fine-tuned 7B model with retrieve-and-re-rank
  and KG-constrained search outperforms ChatKBQA and WikiSP and runs in 2.3 to 14 s per
  question on one consumer GPU (Tables 1, 2; §4).
- With little training data (QALD-7, QALD-10) or hard questions (SPINACH), GRASP with GPT-4.1
  beats GRISP; the authors attribute this to flexible exploration and execution feedback
  (§4, Comparison to GRASP; Table 3).
- Skeleton generation, not placeholder resolution, is the main error source (oracle-skeleton
  analysis, §4).
- Evaluation uses row-wise F1 averaged over samples and EM (§4, Metric).

## My notes

- Fine tuned small language model
- Works by generating a skeleton SPARQL query (placeholders instead of entities or properties)
	- Resolves placeholders left to right - *retrieval-and-rerank* 
	- Constrains the next placeholder based on what was already resolved
	- Backtracking - if finding a placeholder returns `None` it goes back 1 step and tries a different option
- Interesting approach not very relevant to the thesis

## Open doubts

- Your notes say backtracking happens when a placeholder returns `None`; the paper also
  backtracks on empty constrained retrieval and on an invalid final query (§1, §3).
- Not checked: Appendix A split sizes (the HTML table body was not in the fetched text).
- Not checked: how the GRASP search indices are built and whether they transfer to the
  thesis ([AG-02](../questions/AG-02-tool-set.md)).
