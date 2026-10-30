---
id: EV-01
title: Which metrics are reported?
area: evaluation
status: open
phase: agent
priority: medium
depends_on: [LIT-03]
informs: []
---

## Question

What is the primary metric, and which secondary metrics are reported?

## Why it matters

Defines how results are compared with the literature and across configurations.

## Notes

- Decided: execution-based evaluation ([D-007](../decisions.md#d-007)).
- Candidates:
  - row-major F1 (SPINACH; used by GRASP and KGVoyager) and exact match;
  - image-grounding accuracy (gold QID in the top-k of the index; whether the final
    query uses the gold QID);
  - token cost, iterations, wall time and tool-usage statistics, as in KGVoyager.
- The user still wants to read up on and understand these ([LIT-03](LIT-03-kgqa-metrics.md)).
- 2026-10-30: Assistant suggestion, not decided. The draft H3 ([FR-01](FR-01-research-questions.md)) compares
  well-known and less well-known entities, which needs an entity popularity measure,
  e.g. the number of Wikipedia sitelinks. The draft H2 needs answer accuracy given
  correct grounding, to separate grounding errors from query errors.

## Resolution

_Not resolved yet._
