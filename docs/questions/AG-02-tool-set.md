---
id: AG-02
title: Which tools does the agent get?
area: agent
status: open
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

## Resolution

_Not resolved yet._
