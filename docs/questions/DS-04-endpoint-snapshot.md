---
id: DS-04
title: Which Wikidata endpoint and snapshot should be used (WDQS, QLever, dump)?
area: dataset
status: researching
phase: dataset
priority: high
depends_on: []
informs: [DS-02, DS-08, AG-02]
---

## Question

Against which Wikidata endpoint or snapshot are gold queries built and agents
evaluated? The user wants a formal pros/cons comparison.

## Why it matters

Live Wikidata changes over time, so gold answers drift. Endpoint speed and timeouts
also affect the statistics for [DS-02](DS-02-wikidata-subset.md) and agent runs.

## Notes

Options (claims to verify):

- **Live Wikidata Query Service (WDQS):** official and current; query timeout
  (about 60 s); data changes continuously; the graph was reportedly split (scholarly
  articles moved to a separate endpoint), so check what is in the main graph.
- **QLever Wikidata endpoint (University of Freiburg):** very fast for large
  aggregates; used by GRASP and M³-VQA; check update frequency and whether a fixed
  snapshot can be referenced.
- **Local dump (e.g. own QLever instance):** fully reproducible; heavy
  (the full dump is billions of triples).

Whatever is chosen, gold results should be frozen with a date ([DS-08](DS-08-gold-answers.md)).
- 2026-11-06: SPINACH used the live Query Service (60 s limit); QLever on the latest dump failed for their ToG baseline (App. D). Source: [SPINACH note](../literature/liu2024spinach.md).
- 2026-11-06: GRASP uses the public QLever endpoints (§3) and builds its own entity and property search indices from two SPARQL queries per KG (§3.4; Wikidata: 85M entities, 6 GB index, Table 3); SPINACH uses the Wikidata search API. Leaning (user): the Wikidata search API is enough as a search tool, since the thesis is Wikidata-only ([D-003](../decisions.md#d-003)); not decided. Not checked: how the Wikidata API ranks results compared to GRASP's index. Source: [GRASP note](../literature/walter2025grasp.md).
- 2026-11-07: KVQA used a fixed Wikidata RDF dump (2018-05-05) as its snapshot (§Knowledge Graph). Source: [KVQA note](../literature/shah2019kvqa.md).
- 2026-11-13: QAWiki evaluates gold and predicted queries on the live Query Service in the same time frame and lists changing results as a limitation (§4.2, §4.4); no snapshot date. Source: [QAWiki note](../literature/loustaunau2025qawiki.md).

## Resolution

_Not resolved yet._
