---
id: EV-03
title: Which ablations are run?
area: evaluation
status: researching
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
- 2026-11-06: GRASP studies function sets, model provider, model size, feedback and few-shot examples (§4.3, Tables 5 to 8), templates for our ablations. Optional candidate, not committed (user): a feedback step when the agent wants to finish; in GRASP the same model sees only the final call and the SPARQL rules, at most 2 loops (§3.6), and it helps zero-shot but little with few-shot examples (Table 8). Source: [GRASP note](../literature/walter2025grasp.md).
- 2026-11-08: KGVoyager ablations (§4.4, Table 4), each on only 2 to 4 model-benchmark pairs, 3 runs, mean ± std: without `explore_entity_relations` F1 drops by 1.5 to 8.6; without `explore_property_usage` by 12.5, 4.2 and 0.7 (the last within run-to-run variability); keyword-only instead of hybrid retrieval by 1.1 to 26.5. Ideas (user, not decided): removing tools; execution feedback on partial queries as an ablation; hybrid vs. keyword-only entity search. Source: [KGVoyager note](../literature/wisam2026kgvoyager.md).
- 2026-11-08: OVEN's error analysis: 100 random human-set examples categorised by hand into correct, wrong but relevant, too generic, misunderstood query, miscellaneous (Table 3, §6). Option for a short error-analysis section in the thesis, not mandatory (user). Source: [OVEN note](../literature/hu2023open.md).

## Resolution

_Not resolved yet._
