---
id: LIT-03
title: Which evaluation metrics does the KGQA literature use, and how are they computed?
area: literature
status: researching
phase: dataset
priority: high
depends_on: []
informs: [EV-01]
---

## Question

Which metrics do SPINACH, GRASP, KGVoyager and related work report, and how exactly
are they computed?

## Why it matters

Evaluation is execution-based ([D-007](../decisions.md#d-007)), but the details (which columns, ordering,
labels, multiple answers) decide how gold answers must be stored ([DS-08](DS-08-gold-answers.md)).

## Notes

- SPINACH introduced a row-major F1 over result tables; GRASP and KGVoyager adopt it.
  Need to understand how it handles extra columns, column order, labels vs IRIs and
  duplicate rows.
- Also seen: exact match, hits@1 (Mintaka), monetary cost, agent iterations, wall
  time (KGVoyager).
- GRASP reports errors where the question is ambiguous and both the gold and the
  generated query are reasonable; it asks for metrics that are more robust to this.
- 2026-11-06: SPINACH row-major metrics (§5.1): per-row recall ignores extra predicted columns (`|y_i ∩ y_j'| / |y_i|`), rows are matched by an optimal assignment (SciPy `linear_sum_assignment`, zero-recall matches disallowed), F1 = 2tp / (2tp + fp + fn), EM = 1 iff F1 = 1. Columns are compared as sets within a row, so column order does not matter. Baselines that return labels were compared on gold labels instead of IDs (App. D). Not stated: handling of duplicate rows. Still to check: GRASP and KGVoyager. Source: [SPINACH note](../literature/liu2024spinach.md).
- 2026-11-06: GRASP (§4.1): SPINACH's F1 modification (extra predicted columns are not penalised), exact F1 for results over 1,024 rows, ASK vs SELECT counts as 1 if semantically equivalent, samples with empty gold excluded. §4.4: ambiguous questions and different `LIMIT` clauses give unfairly low scores. Source: [GRASP note](../literature/walter2025grasp.md).
- 2026-11-07: M3-VQA scores each question as the IoU of the predicted and gold answer sets, with answer aliases (Wikidata) and a one-year margin for dates; the mean over questions is the final score (paper §4.3, App. G). Consideration only: a SPARQL result is also a set, and matching on Wikidata IDs would remove the need for aliases. Source: [M3-VQA note](../literature/ma2026m3.md).

## Resolution

_Not resolved yet._
