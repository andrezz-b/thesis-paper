---
id: LIT-03
title: Which evaluation metrics does the KGQA literature use, and how are they computed?
area: literature
status: open
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

## Resolution

_Not resolved yet._
