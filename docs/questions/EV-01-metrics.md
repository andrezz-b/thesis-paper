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
- 2026-10-30: Assistant suggestion, not decided. The draft H2 ([FR-01](FR-01-research-questions.md)) compares
  well-known and less well-known entities, which needs an entity popularity measure,
  e.g. the number of Wikipedia sitelinks. The draft H1 needs answer accuracy given
  correct grounding, to separate grounding errors from query errors. (Hypothesis
  numbers updated 2026-10-30 after [D-017](../decisions.md#d-017).)
- 2026-11-06: GRASP uses SPINACH's F1 variant that allows extra columns, averaged over samples, on 200 random samples per benchmark (§4.1); over 1,024 rows it falls back to standard F1; an ASK vs SELECT mismatch scores 1 if semantically equivalent. Source: [GRASP note](../literature/walter2025grasp.md).
- 2026-11-07: ReasonVQA's metrics (exact match, substring, semantic similarity on answer text; §4.3) do not apply to query results; semantic similarity could only matter for comparing label answers. Contrast, see [LIT-03](LIT-03-kgqa-metrics.md). Source: [ReasonVQA note](../literature/tran2025reasonvqa.md).

## Resolution

_Not resolved yet._
