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

## Resolution

_Not resolved yet._
