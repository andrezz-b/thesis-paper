---
id: DS-04
title: Which Wikidata endpoint and snapshot should be used (WDQS, QLever, dump)?
area: dataset
status: open
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

## Resolution

_Not resolved yet._
