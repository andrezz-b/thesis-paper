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

## Resolution

_Not resolved yet._
