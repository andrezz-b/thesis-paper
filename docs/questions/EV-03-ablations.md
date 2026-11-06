---
id: EV-03
title: Which ablations are run?
area: evaluation
status: open
phase: agent
priority: low
depends_on: [DS-10, AG-05]
informs: []
---

## Question

Which factors are varied in ablation studies?

## Why it matters

Ablations support the research questions ([FR-01](FR-01-research-questions.md)), but cost compute time on CampusAI.

## Notes

- Depends on how the dataset work goes.
- Candidates: number and strategy of distractors ([IX-01](IX-01-distractor-strategy.md), [IX-02](IX-02-distractor-count.md)); embedding model
  ([IX-03](IX-03-embedding-models.md)); removing individual tools, as KGVoyager does ([AG-02](AG-02-tool-set.md)); results per question
  type and hop count.
- 2026-11-06: SPINACH ablates by removing each non-essential tool one at a time on the dev set (§5.5, Table 4) and analyses 20 low-F1 cases by error category (§5.4); both are templates. Source: [SPINACH note](../literature/liu2024spinach.md).

## Resolution

_Not resolved yet._
