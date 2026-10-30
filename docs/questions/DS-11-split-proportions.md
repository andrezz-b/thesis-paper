---
id: DS-11
title: How is the dataset split into dev and test?
area: dataset
status: open
phase: dataset
priority: low
depends_on: [DS-01]
informs: []
---

## Question

What proportion goes to dev vs test, and how is the split assigned?

## Why it matters

The dev split prevents tuning prompts and tools on the test set ([D-008](../decisions.md#d-008)).

## Notes

- Decided: dev + test, no train split ([D-008](../decisions.md#d-008)).
- Open: the proportion (suggested 10–20 % dev); stratification by question type and
  domain; whether dev and test entities should be disjoint. The split is assigned at
  generation time and stays fixed.
- 2026-10-30: Rule adopted in the project plan (suggested in review): the test split
  is only used after tuning on the dev split has ended (2027-02-26, [D-015](../decisions.md#d-015)).

## Resolution

_Not resolved yet._
