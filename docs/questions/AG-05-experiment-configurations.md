---
id: AG-05
title: Which agent configurations are evaluated?
area: agent
status: open
phase: agent
priority: medium
depends_on: [AG-04]
informs: [EV-02, EV-03]
---

## Question

Which combinations of "the model sees the image" and "the agent has the image-index
tool" are run?

## Why it matters

Separates how much comes from the model recognising the entity itself from how much
comes from retrieval. Serves as both the baselines and the ablation set, using one
model.

## Notes

Proposed set (the user wants to test without the index, without vision, and with
both):

| Config | Model sees image? | Index tool? | Measures |
| --- | --- | --- | --- |
| Oracle | n/a (entity named in text) | no | upper bound: SPARQL ability alone |
| Vision-only | yes | no | recognition from the model's own knowledge |
| Index-only | no | yes | retrieval-driven grounding |
| Full | yes | yes | combined |

Feasibility depends on [AG-04](AG-04-gemma-hpc.md).
- 2026-11-07: M3-VQA's entity-name oracle (the model is told the entity names, so recognition is removed) matches the oracle configuration here (paper §5.3; average 34.7% vs 24.5% Original, Table 4). An oracle that hands the agent the relevant Wikidata triples (analogue of their Sentence level) is conceivable but unlikely. Source: [M3-VQA note](../literature/ma2026m3.md).
- 2026-11-07: ReasonVQA evaluates 13 vision-language models zero-shot with image + question only, no tools or retrieval (§4.2): the "vision-only" configuration without an agent. Source: [ReasonVQA note](../literature/tran2025reasonvqa.md).

## Resolution

_Not resolved yet._
