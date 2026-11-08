---
key: wisam2026kgvoyager
title: "KGVoyager: Knowledge Graph Agnostic Question Answering via Agentic Navigation"
authors: ["Essam Wisam", "Chengkai Li"]
year: 2026
venue: ""
url: "https://arxiv.org/abs/2609.01780"
pdf: "https://arxiv.org/pdf/2609.01780"
arxiv: "2609.01780"
doi: ""
s2_id: ""
code: ""
data: ""
status: reviewed
relevance: medium
read_depth: full
informs: [AG-02, AG-01, EV-01, EV-03, AG-04, DS-08, DS-13]
themes: [agentic-sparql, kgqa, metrics]
added: 2026-11-06
reviewed: 2026-11-08
candidates:
  - id: "DOI:10.1145/3799682.3839996"
    title: "Benchmarking Agentic Text-to-SPARQL for Multi-Hop Scholarly Knowledge Graph Exploration"
    via: recs
    priority: medium
    scout_priority: high
    why: "Agentic text-to-SPARQL benchmark with researcher-authored multi-hop questions over a DBLP subset; comparison point for agent evaluation and difficulty (EV-02, AG-02, DS-13). Not Wikidata (abstract only)"
  - id: "arXiv:2307.07697"
    title: "Think-on-Graph: Deep and Responsible Reasoning of Large Language Model on Knowledge Graph"
    via: refs
    priority: medium
    why: "Early LLM-as-agent KG exploration; KGVoyager and GRASP both contrast with it (AG-01, AG-02) (abstract only)"
  - id: "arXiv:2507.13859"
    title: "SPARQL Query Generation with LLMs: Measuring the Impact of Training Data Memorization and Knowledge Injection"
    via: refs
    priority: medium
    scout_priority: low
    why: "Measures how much text-to-SPARQL depends on memorised knowledge vs. injected knowledge; Wikidata memorisation confound (AG-04, DS-08) (abstract only)"
bibtex: |
  @misc{wisam2026kgvoyager,
    doi = {10.48550/ARXIV.2609.01780},
    url = {https://arxiv.org/abs/2609.01780},
    author = {Wisam, Essam and Li, Chengkai},
    keywords = {Information Retrieval (cs.IR), FOS: Computer and information sciences},
    title = {KGVoyager: Knowledge Graph Agnostic Question Answering via Agentic Navigation},
    publisher = {arXiv},
    year = {2026},
    copyright = {arXiv.org perpetual, non-exclusive license}
  }
---

# KGVoyager: Knowledge Graph Agnostic Question Answering via Agentic Navigation

Read from the arXiv HTML (v2, 15 Oct 2026). Preprint, no venue stated. The code link in
§1 is an anonymised review repository (`anonymous.4open.science/r/nl2sparql2-C171`), so
`code` is left empty.

## TL;DR

A ReAct-style (think-act-observe) agent that writes SPARQL for an arbitrary RDF graph
given only its query endpoint. Instead of GRASP's index over all entities, it indexes
only the classes (one SPARQL query) and finds entities on demand inside a class. It
beats GRASP by 3.7 F1 points on average on four domain-specific benchmarks at lower
cost. For the thesis it is a design reference for the agent's tools ([AG-02](../questions/AG-02-tool-set.md)), the
metrics ([EV-01](../questions/EV-01-metrics.md)) and the ablation design ([EV-03](../questions/EV-03-ablations.md)); the KG-agnostic goal itself is out of
scope ([D-003](../decisions.md#d-003)), and Wikidata is explicitly not supported.

## Problem and contribution

- Problem: LLM text-to-SPARQL systems rely on ontologies and example text-SPARQL pairs,
  which are often missing for domain-specific KGs (§1: ontology deficiency, opacity,
  example scarcity). Goal: a natural language interface given only query endpoint
  access (§1).
- Contributions (§1): the KGVoyager agent with KG-agnostic tools; evaluation against GRASP
  on four domain-specific benchmarks; open-source release.
- Claimed differences to GRASP (§2): (1) index size: classes instead of all entities
  (Table 1: DBLP 35 classes / 2.7 KB vs. 140.9M entities / 21 GB; SOCKG 91 / 5.3 KB vs.
  7.1M / 1.1 GB); (2) property semantics inferred from data instead of ontology
  domain/range; (3) semantic and keyword search combined jointly (hybrid retrieval)
  instead of used as separate signals.
- Feasibility study (§4.1, Table 2): over 28 okn.us endpoints, the class index could be
  built for 67.9% (Jena) / 96.4% (QLever); GRASP's entity index for 21.4% (Jena) / 0%
  (QLever).

## Method

- Loop: think-act-observe; the prompt asks for search, then explore, then
  construct-and-test (§3, App. G). The final query is submitted via an `answer` tool;
  a `cancel` tool allows early termination, taken from GRASP (§3).
- Only assumptions: instances are typed with `rdf:type` (RDFS), and a class index is
  retrievable with one SPARQL query (§1, App. B).
- Search tools (§3.1):
  - `search_all_classes`: the class index is fetched on first call and cached. Results carry
    label, aliases, instance count and a relevance score.
  - `lookup_class_instances`: finds entities inside a class by lexical SPARQL filter on
    label/IRI (`exact_term`). If that fails, `fallback_term` fetches a larger candidate set
    that is filtered by semantic similarity of labels. `all_attributes` mode searches all
    literal values (slower).
  - `search_all_properties`: all distinct predicates are fetched and cached on first use,
    then searched like classes. Returns labels, aliases, usage counts, domain/range if
    available.
- Hybrid retrieval (§3.1): dense vectors plus sparse BM25, fused with reciprocal rank fusion.
  App. A, Table 5: bge-small-en-v1.5, BM25 top-20, dense top-10, RRF rank constant 61,
  bge-reranker-base top-10 (the text of §3.1 does not mention the reranker).
- Context rot control (§3.1): results whose score relative to the top result is below
  δ = 0.125 are dropped, but the top three are always kept. δ was tuned manually.
- Exploration tools (§3.2): `explore_property_usage` samples triples of a property
  (3000 in App. A) and aggregates subject/object classes and examples; 
  `explore_entity_relations` lists incoming/outgoing properties of an entity with examples.
- Execution tool (§3.3): `execute_query` runs partial or final queries and returns feedback.
- Worked example on DBLP in ten tool calls (§3.4, Fig. 2).

## Data / benchmark

Not a dataset paper; it uses existing benchmarks. For reference (§4.2):

- Is gold SPARQL released? Used for evaluation; question-SPARQL pairs are said to be in the
  repository and a supplementary data file (§4.2). Not checked, the repository is anonymous.
- Is the depicted entity named in the question text? Not applicable (text only).
- Which KG? Climate Models KG (108 questions), SOCKG (98), DREAM-KG (88), DBLP-QuAD
  (100, random sample of the test split). The first three are okn.us KGs with
  QA pairs supplied by the KG developers (§4.2). Snapshot/endpoint: okn.us endpoints
  (Jena); not stated per benchmark.
- Multi-hop, question types: not stated as a taxonomy. App. C measures gold query
  complexity (triple patterns, special constructs: aggregation, FILTER, OPTIONAL, UNION,
  MINUS, EXISTS, subqueries, property paths); DBLP has at most four triple patterns, the others
  mostly five or more.
- Image index, distractors: not applicable.
- Agentic systems evaluated: KGVoyager, GRASP (given its full entity index), and a
  "Grep Ontology" baseline on SOCKG.
- Size, splits, licence: sizes above; no train split used (zero-shot); licence not stated.
- Models: GPT-6 Sol, GPT-OSS-120B, Nemotron 3 Ultra, Muse Glimmer 30B; three runs each
  (§4.2, §4.3).

## Key results

- Average over four benchmarks and four models (Table 3): F1 64.6 vs. GRASP 60.9 (+3.7);
  cost $2.43 vs. $3.94 (-38.3%); iterations 19.6 vs. 23.4; time 85.6 s vs. 112.4 s
  (-23.8%). GRASP gets its best-case entity index.
- Per benchmark F1 (Table 3): Climate 69.8 vs. 67.2; SOCKG 71.3 vs. 68.9; DREAM 49.7 vs.
  46.9; DBLP 67.5 vs. 60.8. DBLP runtime is 19.8% higher than GRASP's (§4.3): entity names
  are resolved in one lookup with the full entity index.
- Per model F1 averaged over benchmarks (App. D): GPT-6 Sol 78.2, Muse Glimmer 30B 69.8,
  Nemotron 3 Ultra 68.4, GPT-OSS-120B 41.9.
- Grep Ontology baseline on SOCKG (Fig. 4, §4.3): 63.2 vs. 71.3 F1 (-8.1), cost 36.4% lower for
  KGVoyager. The authors attribute it to context rot from long grep outputs.
- Ablations (Table 4, §4.4; each on only 2 to 4 model-benchmark pairs): removing
  `explore_entity_relations` lowers F1 by 1.5 to 8.6; removing `explore_property_usage`
  lowers F1 by 12.5 (GPT-OSS, Climate), 4.2 (Muse 30B, SOCKG) and 0.7 (Nemotron, SOCKG;
  within run-to-run variability); keyword-only instead of hybrid lowers F1 by 1.1 to 26.5
  (the largest: GPT-OSS on SOCKG, 46.9 to 20.4).
- Complexity (App. C): the advantage over GRASP shrinks for the most complex queries; pooled
  F1 58.8 vs. 57.4 for seven or more triple patterns.
- Failure analysis (App. F, Table 6): 156 complete failures (F1 = 0 in all three runs): query
  generation/execution 36% (mostly "agent gave up", n = 50, mainly smaller models and
  long contexts), concept resolution 19%, answer representation 18%, query construction
  13%, other 15%.

## Limitations

Authors say:

- Knowledge graphs with their own typing convention, such as Wikidata, are not directly
  supported; adapter tools are future work (Limitations section).
- Few domain-specific text-SPARQL benchmarks exist, so larger datasets could not be
  gathered (Limitations section).
- Generated queries may be valid but semantically wrong (Ethical Considerations).

We see (assistant reading, not stated in the paper):

- Ablations use only a few model-benchmark pairs, and some differences are within noise
  (the authors say so for one pair).
- GRASP's reported numbers come from the authors' own runs of GRASP with a self-built
  entity index; per-benchmark F1 gaps are 2.4 to 6.7 points, with variance only shown in the
  figures.
- All benchmarks are small (88 to 108 questions).
- No Wikidata results at all; the paper does not test open-domain KGs where LLMs know a lot.

## Relevance to the thesis

Proposed, not agreed yet.

- [AG-02](../questions/AG-02-tool-set.md): adopt (ideas) / contrast. The thesis tools are Wikidata-specific ([D-003](../decisions.md#d-003)), so
  KGVoyager's KG-agnostic constraint is dropped. Worth adopting for grounding IDs by
  search instead of recall: a search tool with hybrid retrieval and adaptive score
  filtering (§3.1), property-usage exploration (§3.2), execute-query with partial drafts
  (§3.3), `answer`/`cancel` termination (§3). Tool ablations (Table 4) show which tools
  matter. Execution feedback is also an ablation candidate ([EV-03](../questions/EV-03-ablations.md)).
- [AG-01](../questions/AG-01-own-agent-vs-grasp.md): adopt (as inspiration). The plan is an own implementation; KGVoyager's code and tool
  specifications (App. G) serve as a reference, not a base. Code is only an anonymous link
  so far. The 3.7-point gain over GRASP (Table 3) is not what decides this.
- [AG-02](../questions/AG-02-tool-set.md) (Wikidata): contrast. Porting its class-scoped lookup to Wikidata would need
  adapter tools for P31-style typing (Limitations); judged too much work and not pursued.
- [EV-01](../questions/EV-01-metrics.md) / [LIT-03](../questions/LIT-03-kgqa-metrics.md): adopt. Uses SPINACH's row-major F1 like GRASP (§4.3), and also reports cost,
  iterations, wall-clock time and tool-call counts (Table 3, App. E).
- [EV-03](../questions/EV-03-ablations.md): adopt (idea). Ablation by removing a tool or swapping one component (e.g. hybrid vs.
  keyword-only entity search, with vs. without exploration tools), 3 runs, mean ± std
  (§4.4, Table 4). Their ablations cover only 2 to 4 model-benchmark pairs.
- [DS-08](../questions/DS-08-gold-answers.md): cite. The failure analysis shows that 18% of complete failures are answer
  representation problems (result shape, SELECT vs. ASK, IRI vs. label; App. F,
  Table 9), which matters for how results are compared with the gold result.
- [DS-13](../questions/DS-13-difficulty-levels.md): cite. Gold-query complexity by number of triple patterns and special
  constructs as a difficulty proxy (App. C, Fig. 6).
- [AG-04](../questions/AG-04-gemma-hpc.md): cite. The authors suspect that smaller models give up early because of long
  contexts (App. F; App. D: GPT-OSS-120B 41.9% F1), relevant for the CampusAI model
  choice and for capping tool output length. This is their hypothesis, not tested directly.
- [DS-04](../questions/DS-04-endpoint-snapshot.md): cite, weak. On the okn.us tests the Wikidata class index failed (Jena) or timed out
  (QLever) (Table 2); rdf:type is not used by Wikidata (App. B).

## Citable claims

- Entity-level indexing is often infeasible on public endpoints: GRASP's entity index could
  be built for 21.4% (Jena) and 0% (QLever) of 28 okn.us endpoints, the class index for
  67.9% and 96.4% (§4.1, Table 2).
- A class-only index is orders of magnitude smaller than an entity index: DBLP 2.7 KB vs.
  21 GB (Table 1).
- On four domain-specific benchmarks, averaged over four models, KGVoyager reaches 64.6 F1 vs.
  60.9 for GRASP, at 38.3% lower cost and 23.8% lower runtime (Table 3).
- Hybrid (dense + BM25, RRF) retrieval beats keyword-only search in all four tested
  model-benchmark pairs (+1.1 to +26.5 F1; Table 4).
- Limiting the number of low-scoring results returned by tools is motivated by context rot
  (§3.1); long tool outputs hurt smaller models more (§4.3, grep baseline).
- Most complete failures are not wrong-concept errors: 36% of them are the agent giving up
  or not producing a query (Table 6, Table 10).
- Wikidata is not directly supported by the method because it does not type entities with
  `rdf:type` (Limitations, App. B).

## My notes
- Enable natural language interface given only query access endpoint
- GRASP assumes index covering all entities, KGVoyager needs an index of the classes
	- What is meant by index over classes?
- Possibly use tools for better grounding
	- Even though we are only on Wikidata would allow the model to better grounded and not hallucinate
- Context rot tuning
- Class index not possible for wikidata (listed as timeout)
- SPINACH F1 row major metric
- Ablation study by changing/removing tools
	- What is hybrid retrieval?

## Open doubts

- What is a class index? Answer from the paper: the list of `rdf:type` classes in the KG, fetched
  by one SPARQL query, with label, aliases and instance count (§1, §3.1). It is embedded and
  cached locally. Entities are not indexed; they are looked up inside a class at query time.
- Table 2 for Wikidata: Jena class index failed (x), QLever class index is a timeout (blank),
  both entity indexes failed. The note "timeout" holds only for QLever.
- Is the reranker (App. A, Table 5) used in the search tools? Not described in §3.1.
- Is the code released in a non-anonymous form? Not checked.
- Row-major F1: not defined in this paper, only referenced to SPINACH (§4.3); see the
  SPINACH note.
