---
id: AG-02
title: Which tools does the agent get?
area: agent
status: researching
phase: agent
priority: high
depends_on: [AG-01]
informs: [EV-03]
---

## Question

What exact tool set does the agent use (names, inputs, outputs)?

## Why it matters

The tools are the core of the system design and the subject of ablations.

## Notes

- Expected categories: SPARQL execution; entity and property search; schema or
  neighbourhood exploration; image-index search; final answer and cancel.
- Inspiration:
  - KGVoyager: `search_all_classes`, `lookup_class_instances`,
    `search_all_properties`, `explore_property_usage`, `explore_entity_relations`,
    `execute_query`, answer, cancel.
  - GRASP: execute, list triples, search functions.
  - SPINACH: Wikidata-specific tools.
- Design question: how the image tool refers to the image (an ID handle vs pixels in
  the prompt).
- Endpoint choice ([DS-04](DS-04-endpoint-snapshot.md)) and index payload ([IX-04](IX-04-index-payload.md)) shape the tools.
- 2026-11-06: SPINACH tool set (§4.1): `search_wikidata`, `get_wikidata_entry` (outgoing edges and qualifiers, pruned by a separate LLM prompt), `get_property_examples`, `execute_sparql` (returns results, empty, syntax error text or timeout; long results truncated to first and last 5 rows) and `stop`. Removing a tool one at a time lowers dev F1 from 46.4 to 36.4 (entry), 29.4 (property examples), 25.3 (search) (Table 4). Leaning (user): the image-index search is one more tool in the same loop. Source: [SPINACH note](../literature/liu2024spinach.md).
- 2026-11-06: GRASP tool set (§3.2, Table 1): `answer`, `cancel`, `execute` (more than 10 rows or columns: first and last 5 shown; 60 s timeout), `list` triples (max 10, diverse), `search_entity` (prefix-keyword index), `search_property` (embedding index), `search_property_of_entity`, `search_object_of_property`; search tools return the top 10. Function-set study with Qwen2.5 72B (Table 6): execute-only is worst everywhere (e.g. SPINACH benchmark 17.3 vs 27.6 with the full set); the set with property-of-entity and object-of-property search is best overall; the more flexible `search_autocomplete` and `search_constrained` were harder for the model to use (§4.3). Open: map GRASP's tools to SPINACH's (`search_wikidata`, `get_wikidata_entry`, `get_property_examples`, `execute_sparql`) and see which can be simplified or combined. Source: [GRASP note](../literature/walter2025grasp.md).
- 2026-11-07: M3-VQA's agent executor has object detection (Qwen2.5-VL-7B), text retrieval and image retrieval tools under a planner (paper §5.4, App. F.2). Source: [M3-VQA note](../literature/ma2026m3.md).
- 2026-11-08: KGVoyager detail (§3.1 to §3.3, App. A): the class and property indexes are fetched with one SPARQL query on first use and cached; search uses dense + BM25 retrieval fused with reciprocal rank fusion, then an adaptive filter that drops results scoring below 12.5% of the top one (always keeping three) to limit context rot; `explore_property_usage` samples 3000 triples of a property. Its class-scoped instance lookup relies on `rdf:type`, which Wikidata does not use for typing, so a port would need adapter tools (Limitations, App. B); too much work, not pursued (user). Idea (user, not decided): tools help ground IDs by search instead of recall, and execution feedback on partial queries is an ablation candidate ([EV-03](EV-03-ablations.md)). Consistent with [D-003](../decisions.md#d-003). Source: [KGVoyager note](../literature/wisam2026kgvoyager.md).
- 2026-11-13: KnowCoL uses the Wikidata graph as a training signal (KG embeddings), not at inference (Eq. 12); our agent queries the graph with tools. Its ablation shows the type hierarchy (P31, P279, P171) matters most for unseen entities: HM 31.5 to 28.3, unseen 29.1 to 25.3 (Table 3). No change to the tool set. Source: [KnowCoL note](../literature/zhou2025seeing.md).
- 2026-11-15: GRISP is not an agent, but its KG guidance (§1, §3) restricts the index search for the next placeholder to IRIs returned by a SPARQL query built from the already resolved part (e.g. only properties that occur for the resolved entity). This is the same idea as GRASP's `search_property_of_entity` and `search_object_of_property`, now used inside a trained pipeline; ablation on WWQdev: removing constrained search 84.4 to 83.2 F1, removing KG guidance (also the final query validation) to 80.7 (Table 5). Authors conjecture a larger effect on KGs with a more complex schema (§4). Supports keeping the property-of-entity search tool; no change to the tool set (assistant reading). Source: [GRISP note](../literature/walter2026grisp.md).
- 2026-11-21: Current GRASP adds an automatic setup (§3.1): agent-written exploration notes (structural, then functional, i.e. how each tool behaves) appended to the context, and a shape index of ShEx-like class shapes (properties with value types; top 500 classes, others on the fly) searchable at inference; also literal search and an answer function that takes SPARQL plus a human-readable answer. The user found the notes-as-context and shape-index ideas most useful; not decided. Notes do not help uniformly: self-QA notes -2.7 F1 for GPT-5.4, samples notes +5 on English test, +0 on Spanish (§4). Source: [GRASP/WikiKGQA note](../literature/walter2026grasp.md).
- 2026-11-21: LLM-RA shows that cropping question-relevant entity regions (LLM picks entities from a caption, Grounding-DINO returns boxes) before retrieval improves Recall@5 over whole-image queries, random or evenly split crops, and all detected objects (Table 4; OK-VQA 87.24 to 90.30, InfoSeek 39.78 to 47.31), and a pipeline of existing components beat an end-to-end grounding VLM (Table 5). An image crop/ground tool is a candidate (user: yes, a good idea). If adopted, the user prefers the agentic detection plus per-segment image retrieval of M3-VQA (§5.4), which fits our agent approach better; LLM-RA itself has many extra parts (captioner, entity prompt, grounder, trained retriever), so it is only cited as evidence that cropping helps. Not decided. Source: [LLM-RA note](../literature/jian2024large.md).
- 2026-11-21: PMSR (Choi et al., ACL 2026) is a fixed workflow: describe the image, retrieve, condense the evidence into a short record, write a record-level and a trajectory-level query from it, repeat up to 5 times, stop when new queries repeat earlier ones (§3, Eq. 9-10). Each record is built only from newly retrieved evidence. This is an approach the agent could take for grounding the depicted entity with the image index. Leaning (user): a nice thing to have and test, ideally a switch that runs the agent in this mode, but it would be real work and the user does not feel confident committing to it given the other challenges and time constraints. Not decided. Source: [PMSR note](../literature/choi2025progressive.md).
- 2026-11-22: SAGE-VQA adds a verification step to the detect, crop, retrieve flow (§3.2, App. A.3, A.7): SAM3 proposes regions from text prompts, the VLM checks each masked crop against its prompt (`is_match` plus confidence, then a comparison with its whole-image observations), and only verified box crops go to the image-index search (CLIP, 2 nearest images per crop); failed crops stay visible to the reasoner with a flag. Leaning (user, not decided): take verify-then-retrieve as an extension of the M3-VQA crop flow, and merge SAGE's two checks (crop vs prompt, local vs global) into one "check" call. Cost: one extra VLM call per candidate crop (App. A.6). Caveat: the paper's "+EDAR" ablation bundles verification with a readiness loop (97.97% of ScienceQA questions stop after one iteration), so the effect of verification alone is not measured (App. E, Table 5). The paper's memory system is out of scope (user). Source: [SAGE-VQA note](../literature/shen2026sage.md).

## Resolution

_Not resolved yet._
